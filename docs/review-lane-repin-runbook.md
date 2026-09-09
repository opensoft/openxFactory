# Advancing the pinned decision core — the hand cycle and the lane that replaces it

Status: draft
Kind: runbook
Repository context: openxFactory
Backed by: `openspec/changes/mirror-floor-regeneration-automation/` (ratified
  2026-09-06, record
  [`ratification-2026-09-06.md`](../openspec/changes/mirror-floor-regeneration-automation/review/ratification-2026-09-06.md)),
  whose eight ADDED requirements this runbook describes in operational terms.
  Its codexFactory parent is `add-floor-regeneration-automation` (codexFactory
  #235), which automates the OTHER half of the same repair.

**Why this document is `draft` and not `ratified`.** The lane it describes is
ratified and realized, but `tasks.md` § 5 — the first UNATTENDED cycle, observed
end to end — is open by design, and § 5.7 asks for one observed refusal on a
real run before the automation is treated as proven. Until a real cycle is
recorded here, this runbook documents a mechanism that has been tested but not
yet watched. The section [What is not yet proven](#what-is-not-yet-proven) says
exactly what is missing.

## What this is about, in one paragraph

This repository is judged by a decision core that lives in **codexFactory**, and
it names the codexFactory commit doing the judging in **five places**. When
codexFactory's floor document moves — because a new `openspec/specs/**` path
landed here and had to be added to the floor — those five places have to move
together, or the vendored copy stops matching the document it claims to witness.
Doing that by hand is transcription: one commit id into four places and a digest
into a fifth. `.github/workflows/review-lane-repin.yml` now proposes it.

## The five sites

They are one list in code — `PINNED_SITES` in
[`scripts/review_lane_repin.py`](../scripts/review_lane_repin.py) — and a test
sweeps the tree for a sixth
(`tests/review_lane_pin/test_repin_lane.py::TheSiteListIsTheWholeTruth`), so a
site added later fails a test instead of quietly going stale.

| # | site | what it carries |
|---|---|---|
| 1 | `contracts/review-lane-pin.yaml` | `core_commit` |
| 2 | `.github/workflows/merge-master-approval.yml` | `PINNED_CORE_COMMIT` |
| 3 | `.github/workflows/merge-master-approval.yml` | the core checkout `ref:` |
| 4 | `.github/workflows/pytest-suite.yml` | the core checkout `ref:` |
| 5 | `contracts/review-lane-floor-snapshot.yaml` | the byte copy, plus `floor_snapshot.sha256` and `floor_snapshot.entry_count` declared beside the pin |

**All five, or none.** A partial advance is refused by the ratified requirement
*"The mirror is inert until the pin carries the rule, and the pin moves as one
act"*, and the lane cannot author one: it re-reads every site from disk after
writing and discards the whole run if any one of them does not read the new
commit.

## The bot cycle (what happens now)

1. **codexFactory's floor document moves** on its default branch — by its own
   regeneration lane, or by a hand act. Either is enough; see step 2.
2. **The re-pin lane fires.** Its `schedule:` (hourly, at :17) is the
   MECHANISM; the `repository_dispatch` leg (`floor-regenerated`) is only an
   accelerator, and **its payload is never read**. The lane resolves
   codexFactory's default branch and head itself, on every firing, through
   `gh api`. A trigger cannot choose which tree judges this repository.
3. **It refuses, or it measures.** It refuses when: the declared credential
   binding does not resolve; codexFactory's default branch cannot be resolved;
   the candidate commit is not reachable from that branch; or the floor document
   cannot be fetched at it. Every refusal is loud and exits non-zero.
4. **Nothing owed is a named no-op.** When the vendored snapshot is already
   byte-identical to the authoritative document, the run says so and exits 0.
   This is the common case, most hours.
5. **Otherwise it advances all five sites, then re-reads them**, re-copies the
   snapshot from the codexFactory checkout, and recomputes `sha256` and
   `entry_count` **from the bytes it wrote** — never from anything codexFactory
   reported about itself.
6. **It submits itself to the judge before proposing.** It checks codexFactory
   out at the CANDIDATE commit and runs `tests/review_lane_pin` unmodified. A
   bad advance fails the run instead of becoming a red pull request.
7. **It opens ONE pull request on `bot/review-lane-repin`** with the witnesses
   in the body, and stops. A firing that finds that pull request already open
   updates it; it never opens a second.
8. **A human merges it.** The lane never merges, never approves, never enables
   auto-merge and never writes to `main`.

### What the human still does

**Read the witnesses and merge — or don't.** The judgment the lane does not
make is *is this the core commit we mean to be judged by?*, and that is the
whole reason merge authority is unchanged
(`proposal.md` decision M-5). `contracts/review-lane-pin.yaml` is itself a
never-clearable floor entry in codexFactory's floor, on the stated ground that a
clearable pin *"would let a pull request choose its own judge"*; a lane that
could both propose and land a change to it would be exactly that.

The pull-request body carries everything needed, and every value in it is
recomputable — the body prints the three commands. Check:

- the codexFactory commit, and that the body's `compare` evidence shows it on
  codexFactory's default branch;
- `core_commit` before → after;
- the snapshot's `sha256` and `entry_count` before → after;
- the generated block's `generated_at` and entry count before → after;
- the covered-pending paths the advance is expected to clear.

## The hand cycle (still supported, and still required when the lane refuses)

The lane replaces the transcription, not the operator. Do this when the lane has
refused, when the credential is unavailable, or when you need an advance now.

```sh
# 1. Resolve the codexFactory commit and CONFIRM IT IS ON THE DEFAULT BRANCH.
gh api repos/opensoft/codexFactory --jq .default_branch
CORE=$(gh api repos/opensoft/codexFactory/commits/main --jq .sha)
gh api "repos/opensoft/codexFactory/compare/main...${CORE}" --jq .status   # identical|behind

# 2. Re-copy the snapshot. NEVER hand-edit it: it is a witness.
#    FETCH TO A TEMPORARY FILE AND PROVE IT BEFORE IT LANDS ON THE WITNESS.
#    Redirecting `gh api` straight into the snapshot writes an EMPTY file over
#    it when the read 404s, which is the one edit this file must never suffer.
#    THE PATH MOVED on 2026-09-09 (codexFactory #297 -> 8165d1f3, its
#    `relocate-review-authority-floor`). At a CORE older than that the document
#    is at scripts/merge_master/openxfactory-review-authority-floor.yaml, and
#    you set FLOOR to it DELIBERATELY: there is no automatic fallback here for
#    the same reason the lane's declared list is one entry again — a command
#    that quietly accepts either home cannot tell a relocation from a file
#    somebody put back.
FLOOR=floor/openxfactory-review-authority-floor.yaml
FETCHED="$(mktemp)"          # resolved at run time: no host path is committed
gh api "repos/opensoft/codexFactory/contents/${FLOOR}?ref=${CORE}" \
  -H "Accept: application/vnd.github.raw" > "${FETCHED}"
test -s "${FETCHED}" || { echo "no floor document at ${FLOOR}@${CORE} — STOP"; exit 1; }
cp "${FETCHED}" contracts/review-lane-floor-snapshot.yaml
rm -f "${FETCHED}"

# 3. Recompute the two declared witnesses FROM THE BYTES YOU JUST WROTE.
sha256sum contracts/review-lane-floor-snapshot.yaml
python3 -c "import yaml;print(len(yaml.safe_load(open('contracts/review-lane-floor-snapshot.yaml'))['floor']['never_clearable_paths']))"

# 4. Move the four commit sites and the two witness fields, then READ THEM BACK.
python3 -c "
import pathlib, sys; sys.path.insert(0,'scripts')
import review_lane_repin as R
for s in R.PINNED_SITES + R.SNAPSHOT_WITNESS_SITES:
    print(f'{s.label:50s} {R.read_site_value(pathlib.Path(\".\"), s)}')"

# 5. Prove it before you push.
PINNED_CORE_CHECKOUT=/path/to/codexFactory-at-$CORE python3 -m pytest tests/review_lane_pin -q
```

Step 4's read-back is not optional and not decorative: the archived
`mirror-floor-addition-grace` recorded the same discipline as an operator
practice — *"verify each by reading it back rather than by trusting the edit"* —
and the lane exists because a machine cannot record a practice.

**All five sites move in ONE commit.** Do not split them across commits, and do
not open a pull request carrying four of them.

## The credential

The lane runs under the App already installed in both repositories, declared as
a template with no live value in
[`contracts/review-lane-repin-binding.template.yaml`](../contracts/review-lane-repin-binding.template.yaml).

It needs, and the binding declares, exactly:

| repository | permissions | why |
|---|---|---|
| `opensoft/codexFactory` | `contents: read` | resolve the default branch, fetch the floor document |
| `opensoft/openxFactory` | `contents: write`, `pull-requests: write`, `workflows: write` | push `bot/review-lane-repin` — including the two pinned sites that live in `.github/workflows/` — and open and update the one pull request |

`workflows: write` is not decorative. Two of the five pinned sites are workflow
files (the core checkout `ref:` in `merge-master-approval.yml` and
`pytest-suite.yml`), and GitHub refuses an App push that touches
`.github/workflows/**` without that permission — run 34033398015 (2026-09-06)
advanced all five sites and passed the judge, then was refused at the push with
exactly that message. The permission has to exist in TWO places: on the
`openxfactory` GitHub App's installation (App settings → Permissions →
Repository permissions → Workflows → Read and write, then accepted on the org
installation — an owner's act), and on the lane's mint (`permission-workflows:
write`, scoped to this repository only). Without the installation grant the
mint itself refuses with a named error; the lane never degrades to a token that
could push part of an advance.

**It has no write privilege over codexFactory and is declared not to have one.**
That is stated as a refusal in the binding so a later widening has to delete a
line rather than merely fail to add one.

**The lane refuses rather than falling back.** There is no `|| github.token`
anywhere in it, and the reason is specific: a fallback identity cannot read
codexFactory, so the lane would compare the pin against nothing, find no
disagreement, and report a clean no-op. **A missing credential must not be able
to look like a clean run.**

## Firing it by hand

```sh
# An inspection. Measures, writes into the runner's checkout, re-reads every
# site -- and pushes nothing, opens nothing.
gh workflow run review-lane-repin.yml -f dry_run=true

# The real thing.
gh workflow run review-lane-repin.yml -f dry_run=false
```

A dry run still performs the write and the re-read, deliberately: a dry run that
skipped them would prove nothing about them.

## What is not yet proven

Recorded here rather than left to be discovered:

- **No unattended cycle has been observed end to end.** `tasks.md` § 5 is open.
  Everything above is proven by tests and by the two hand cycles of 2026-09-05
  (PRs #689 and #702), not by a watched bot run.
- **No refusal has been observed on a real run** (§ 5.7). Every refusal in this
  runbook is driven by a unit test against a fixture built from the real files;
  none has yet fired in anger.
- **This repository had no `schedule:` in any workflow before this lane.** The
  nightly doc-health run is scheduled by a thin caller in the xFactory
  aggregation repository and reaches here through `workflow_call`. The hourly
  cron is a first for this repository and should be watched for the first few
  days.
- **The other half of the cycle is codexFactory's** and lands separately. Until
  it does, the regeneration is still a hand act and this lane halves the cycle
  rather than closing it.
