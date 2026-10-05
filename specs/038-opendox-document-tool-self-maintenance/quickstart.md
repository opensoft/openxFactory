# Quickstart: running AT-R2, release 2's acceptance

Status: draft

**Feature**: [`spec.md`](./spec.md) FR-024 and SC-008 define the test (R2Q24 (a),
`#656` `6003486656`). T080 automates the HTTP half as a harness in
openDox-code's own `acceptance` CI job (the CI owner's last edit to
`validate.yml`). T081 runs the browser half on the host. Both follow AT-R1's
form (plan 034 `quickstart.md`, T095 and T096), and this file leans on that
one for every step AT-R1 already proved (the free-port check, the console token
read from the private copy's fragment and sent over stdin).

**AT-R2 proves four outcomes** (FR-024), on a clean machine with only
`opendox[local]` and a plain repository:

1. the Health view lists findings, new first;
2. a mechanical repair is drafted from the view, and landed through the view's
   confirm control as a revertible merge commit;
3. an exception survives `runtime reset`;
4. a branch is submitted to a bare remote with `gh` absent.

**The two commits.** The run installs openDox-code at `RELEASE2_TIP`, T080's
landing commit on openDox-code's `main` (X). T084 publishes P, the commit T062
pins (the 0.2.0 bump, T061). Before the publish, T084 checks that the package's
build inputs are identical at P and X (`git diff --quiet P X -- src/
pyproject.toml migrations/ README.md LICENSE`, plan 034 T099's check). If they
differ, both halves run again at P.

Every step depends only on answered questions (R2Q1–R2Q25, `6003486656`) and on
this plan's decisions as Brett rules them (T004). Until the cut, the openDox
root README's install line reads `pip install "./code[local]"`; after it, the
PyPI line.

## 1. A clean machine, with openDox and nothing else, and no `gh`

```sh
set -euo pipefail
W=$(mktemp -d)                                        # scratch space, resolved at run time
: "${RELEASE2_TIP:?set RELEASE2_TIP to T080's landing commit (X), or to P for T084's re-run}"
git clone -q https://github.com/opensoft/openDox-code "$W/openDox-code"
git -C "$W/openDox-code" checkout -q "$RELEASE2_TIP"
python3 -m venv --clear "$W/v"
. "$W/v/bin/activate"
pip install -q "$W/openDox-code[local]"
# gh absent, by PATH (OQ-12-16): a bin directory holding only what the run needs
mkdir "$W/bin"
for t in git python3 curl opendox opendox-runtime; do ln -s "$(command -v "$t")" "$W/bin/$t"; done
export PATH="$W/bin:/usr/bin:/bin"
rc=0; command -v gh >/dev/null || rc=$?
test "$rc" -eq 1 || { echo "FAIL: gh is reachable"; exit 1; }
export OPENDOX_INSTALL_MODE=local OPENDOX_STATE_DIR=$(mktemp -d)
```

If `/usr/bin` holds `gh` on the machine, the bin directory is the WHOLE PATH
instead, and the check above proves it either way.

## 2. A plain repository on `main`, a bare remote, and the declaration

```sh
R="$W/repo"; B="$W/remote.git"
cp -r "$W/openDox-code/tests/fixtures/health-corpus" "$R"
git -C "$R" init -q -b main                          # main, by name: AT-R2's "new first" needs a baseline (I-2)
mkdir -p "$R/.opendox"
printf 'schema_version: 1\nkind: opendox-governance\ngovernance: standalone\n' > "$R/.opendox/governance.yaml"
git -C "$R" add -A && git -C "$R" commit -qm fixture
git init -q --bare "$B"
git -C "$R" remote add origin "$B"
```

## 3. The HTTP half (T080)

Start the server with the one documented command, under `--local`, and read the
console token exactly as AT-R1's § 3 does (the private copy's fragment, sent on
stdin). `H` below stands for that header-on-stdin form.

```sh
PORT=8080                                             # AT-R1 § 3's free-port check runs first
opendox generate-and-open --local --repo-root "$R" --repository fixture --no-open --port "$PORT" &
SERVER=$!                                             # § 5 stops it; set -u needs it set here
trap 'kill "$SERVER" 2>&- || true' EXIT
# … AT-R1 § 3: wait for ready, read TOKEN from the private copy …
curl -sf "http://127.0.0.1:$PORT/capabilities" > "$W/caps.json"
# health is available and land is offered (standalone). caps.health.packs is RECORDED, not asserted:
# FR-024's four outcomes need no pack, and the acceptance job is not a provisioned sandbox host
H POST /actions/health/run        > "$W/run1.json"     # the first default-tip run: every finding new
H POST /actions/health/run        > "$W/run2.json"     # a second run: the baseline now exists
H GET  /health/findings           > "$W/f.json"
```

Assert, in one Python block reading the saved files:

- **Outcome 1.** `caps["health"]["available"]`, `caps["actions"]["submit"]` and
  `caps["actions"]["land"]` are true, and `caps["health"]["actions"]` lists every
  action the view offers (14.5). The findings list is ordered new first; after one new commit that plants
  a fresh broken link, a third run lists that finding `new` ahead of the
  `persistent` ones. No finding's `evidence` holds a string over 200 characters
  or an `excerpt`/`text`/`content`/`quote` key (R2Q25 (a)), and every finding has
  `pack_id` and `pack_version`. No `message` exceeds 200 characters (ADV-27).
- **Outcome 2.** `POST /actions/health/fix` with the `broken-link` finding's id
  answers a draft branch `health-fix-<id>`; `main` has not moved. `POST
  /actions/session/land-nonce` for that branch answers a nonce bound to its head;
  `POST /actions/session/land` with it answers `Landed`. Then: `main`'s tip is a
  merge commit whose first parent is the old `main`; a second `land` with the
  same nonce is refused; and in a scratch clone, `git revert -m 1 --no-edit
  <merge>` succeeds and its tree equals the old `main`'s (`git diff --quiet`).
  Nothing was pushed: `git -C "$B" rev-parse --verify --quiet main` fails.
- **Outcome 3.** `POST /actions/health/accept` for the fixture's accepted finding
  writes `health/dispositions.yaml` (`git status --porcelain` shows it); commit
  it; re-run; the finding is ABSENT. `opendox-runtime runtime reset --confirm
  yes-drop-the-coordination-database`, then `runtime migrate`, then a run: the
  list still holds `broken-link`-class findings and the accepted one is still
  ABSENT (grep's exit status 1 exactly, as F14.1 asserts).
- **Outcome 4.** `POST /actions/session/submit` for a branch made with git
  answers a `Submission` whose `remote` is `origin`, whose `ref` ends with the
  branch's name and whose `url` names `$B` (12.1a's fields), and
  `git -C "$B" rev-parse "refs/heads/<branch>"` equals the branch's tip. With
  `origin` removed, the same call answers the `NoSubmissionTarget` refusal,
  naming the missing remote.

Every listing is saved to a file first and read second, and an absence is
asserted as an exit status, never as `! grep` (F14.1's rule). T080 also requests
every route the Health view and the branch-actions controls call when they load,
and requires that none answers 5xx.

## 4. The browser half (T081)

On the host, with the server from § 3 running against a fresh copy of § 2's
repository, opened through the command's private copy (so the token travels in
the fragment):

1. Open the Health view. The findings are listed new first; each row's passage
   is read from git, and no label renders as HTML.
2. Choose the broken link's repair. A draft branch appears; `main` is unmoved.
3. Land it with the confirm control. The control shows the branch and head it
   confirms; after confirming, `main` holds a merge commit, and the control
   cannot be re-used.
4. Accept the fixture's accepted finding with a reason, commit the file with
   git, reset the store from the terminal, re-run from the view: the finding is
   still gone.
5. Submit a branch to the bare remote from the view; the report names `origin`
   and the remote holds the branch.

Record each step's outcome, with a screenshot, in `evidence/at-r2/`, and the
`RELEASE2_TIP` it ran at.

## 5. Tear down

```sh
kill "$SERVER"
wait "$SERVER" 2>&- || true
rm -rf "$W" "$OPENDOX_STATE_DIR"
```

The bundled datastore stops with the entry point (R1Q16 (iv)), as in AT-R1, and
T080 asserts that no bundled-server process is left.
