#!/usr/bin/env bash
# AT-R1, BOTH halves, at ONE openDox-code commit (plan 034 T096; and T099's
# re-run at P when P's build inputs differ from X's, holder ruling H3 (b) on
# Copilot r4174344151, openxFactory#1225).
#
# For openxFactory specs/034-opendox-standalone-operation/evidence/at-r1/.
# Lane openxfactory-4 wrote it for its t096-dry run; lane openXfactory-3
# (slice D6) adapted it to quickstart.md as it stands on main, and to T104's
# start as openDox-code#84 has it. Bookkeeping: no `Arc:` trailer (R1Q20 (a)).
#
#   usage: run-at-r1.sh P
#     P  the openDox-code commit to measure (a full or short sha, or a ref):
#        X, T095's landing commit on main, for T096's own run; or P, the
#        commit T087 pins, for T099's re-run when P's build inputs differ.
#   It prints ONE verdict line per half, and writes them to $OUT/verdict.txt:
#     AT-R1 HTTP half    at <P>: PASS|FAIL (<the harness's own last line>)
#     AT-R1 browser half at <P>: PASS|FAIL ((a) ...; (b) ...)
#
#   env  ODC_URL     where to clone openDox-code from (default the GitHub repo;
#                    a local clone path works, for a dry run of an integration)
#        AGAINST     optional: X, the commit AT-R1 already ran at. Records
#                    T099's P-against-X step, `git diff --quiet P X -- src/
#                    pyproject.toml migrations/ README.md LICENSE`, and its
#                    exit status, beside the verdicts.
#        PORT        the documented start's --port (default 8080, as quickstart § 3)
#        DRV_PYTHON  a python with playwright, PyYAML and Chromium; built
#                    into the scratch space when unset, with
#                    playwright==$PLAYWRIGHT_VERSION (default 1.63.0). Its
#                    Chromium goes to PLAYWRIGHT_BROWSERS_PATH, or, where
#                    that cache cannot be written, to the scratch space
#        OUT         where the record goes (default $W/out)
#        HALVES      which halves to run (default "http browser")
#        HARNESS_FROM optional: the commit whose acceptance/at_r1_http.py runs
#                    the HTTP half (X, for T099's re-run at P); its full sha
#                    and the harness file's sha256 are recorded
#        TMPDIR      choose a SHORT directory only you can write: the bundled
#                    server's socket path may not pass 107 bytes, and it
#                    refuses a state directory below a world-writable,
#                    non-sticky one (T095's harness reads TMPDIR the same way)
#
# What it runs, in order, all in the foreground:
#   0. a fresh clone of openDox-code at the commit; its full sha is recorded;
#   1. the HTTP half: T095's harness, `python3 acceptance/at_r1_http.py
#      --keep-going`, AS IT IS AT THAT COMMIT (the harness installs its own
#      venv from the commit's tracked files), or, with HARNESS_FROM, as it is
#      at that other commit, copied into this checkout (T099's re-run at P:
#      "The HTTP half runs with T095's harness, as it is at X, against P's
#      checkout"; the harness's own docstring: "to measure another tree, copy
#      this file into it"). The copy is removed again before the browser half;
#   2. the browser half: quickstart.md §§ 1-5 as openxFactory#1222 and #1225
#      amend them, once per repository, (a) 5.0's plain-documents fixture and
#      (b) three Markdown notes with no front matter, with § 4 driven by
#      at_r1_browser.py (beside this file) and judged by the commit's own
#      tests/smoke_signals.py.
# Exit 0 only when the harness exits 0 AND both browser passes pass.
set -euo pipefail
export LANG=C.UTF-8 LC_ALL=C.UTF-8
# GNU grep, resolved at run time: the first `grep` on the PATH that reports
# itself as GNU grep, where a host puts another first (ugrep reads some
# patterns differently). Without one, the PATH's own grep is used. No path is
# named here (openxFactory's constitution, Principle IV; Copilot on #1241).
GNU_GREP=
while IFS= read -r candidate; do
  case "$("$candidate" --version 2>/dev/null | head -1)" in *"GNU grep"*) GNU_GREP=$candidate; break;; esac
done < <(type -aP grep)
if [ -n "$GNU_GREP" ]; then grep() { "$GNU_GREP" "$@"; }; fi
SERVER=
stop_server() {
  if [ -n "$SERVER" ]; then kill "$SERVER" 2>/dev/null || true; wait "$SERVER" 2>/dev/null || true; SERVER=; fi
}
trap stop_server EXIT
for v in $(env | sed -n 's/^\(GIT_[A-Za-z0-9_]*\)=.*/\1/p; s/^\(XF_[A-Za-z0-9_]*\)=.*/\1/p'); do unset "$v"; done
unset OPENDOX_DATABASE_URL OPENDOX_MIGRATION_DATABASE_URL OPENDOX_OIDC_ISSUER OPENDOX_INSTALL_MODE \
      OPENDOX_STATE_DIR DATABASE_URL PGHOST PGPORT PGDATABASE PGUSER

COMMIT=${1:?usage: run-at-r1.sh P (the openDox-code commit to measure)}
HALVES=${HALVES:-http browser}
HERE=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
DRIVER=$HERE/at_r1_browser.py
ODC_URL=${ODC_URL:-https://github.com/opensoft/openDox-code}
PORT=${PORT:-8080}
W=$(mktemp -d)
OUT=${OUT:-$W/out}
mkdir -p "$OUT"
LOG=$OUT/run.log
exec > >(tee -a "$LOG") 2>&1
say() { printf '%s %s\n' "$(date -u +%H:%M:%SZ)" "$*"; }

# ---- 0. the commit ----------------------------------------------------------
say "scratch $W; record $OUT"
git clone -q "$ODC_URL" "$W/openDox-code"
# The argument is a commit-ish (a full or short sha, or a ref): it is resolved
# to ONE commit first, and the checkout must land on exactly that commit. Only
# an abbreviated sha is also held to be a prefix of what it resolved to
# (Copilot r4185918186 on openxFactory#1241: a ref never prefixes a sha).
WANT=$(git -C "$W/openDox-code" rev-parse --verify -q "$COMMIT^{commit}") \
  || { say "FAIL: $COMMIT names no commit in $ODC_URL"; exit 2; }
git -C "$W/openDox-code" checkout -q "$WANT"
P=$(git -C "$W/openDox-code" rev-parse HEAD)
[ "$P" = "$WANT" ] || { say "FAIL: $COMMIT resolved to $WANT, but the checkout is at $P"; exit 2; }
if [[ "$COMMIT" =~ ^[0-9a-f]{4,40}$ ]]; then
  case "$P" in "$COMMIT"*) ;; *) say "FAIL: the abbreviated sha $COMMIT resolved to $P"; exit 2;; esac
fi
test -z "$(git -C "$W/openDox-code" status --porcelain --ignored)"
say "openDox-code $P (from $ODC_URL), a clean checkout"
{
  echo "commit $P"
  echo "from $ODC_URL"
  echo "started $(date -u +%FT%TZ)"
  echo "python3 $(python3 -c 'import sys; print(sys.version.split()[0])')"
  echo "host $(uname -srm)"
} > "$OUT/commit.txt"
if [ -n "${AGAINST:-}" ]; then
  git -C "$W/openDox-code" fetch -q origin "$AGAINST" 2>/dev/null || true
  set +e
  git -C "$W/openDox-code" diff --quiet "$P" "$AGAINST" -- src/ pyproject.toml migrations/ README.md LICENSE
  rc=$?
  set -e
  echo "P-against-X: git diff --quiet $P $AGAINST -- src/ pyproject.toml migrations/ README.md LICENSE -> exit $rc" | tee -a "$OUT/commit.txt"
fi

# ---- 1. the HTTP half: T095's harness, at this commit (or HARNESS_FROM's) -----
HTTP_RC=2
HTTP_LINE="not run"
HARNESS=$W/openDox-code/acceptance/at_r1_http.py
COPIED_HARNESS=0
HARNESS_AT=$P
case " $HALVES " in *" http "*) RUN_HTTP=1;; *) RUN_HTTP=0;; esac
if [ "$RUN_HTTP" = 1 ] && [ -n "${HARNESS_FROM:-}" ]; then
  git -C "$W/openDox-code" fetch -q origin "$HARNESS_FROM" 2>/dev/null || true
  HARNESS_AT=$(git -C "$W/openDox-code" rev-parse --verify -q "$HARNESS_FROM^{commit}") \
    || { say "FAIL: HARNESS_FROM $HARNESS_FROM is not a commit in this clone"; exit 2; }
  if [ "$HARNESS_AT" != "$P" ]; then
    git -C "$W/openDox-code" cat-file -e "$HARNESS_AT:acceptance/at_r1_http.py" 2>/dev/null \
      || { say "FAIL: $HARNESS_AT holds no acceptance/at_r1_http.py"; exit 2; }
    if [ -e "$HARNESS" ]; then say "NOTE: $P has its own harness; T099 runs X's, so the HTTP half runs $HARNESS_AT's"; fi
    mkdir -p "$W/openDox-code/acceptance"
    git -C "$W/openDox-code" show "$HARNESS_AT:acceptance/at_r1_http.py" > "$HARNESS"
    COPIED_HARNESS=1
  fi
fi
if [ "$RUN_HTTP" = 1 ] && [ -f "$HARNESS" ]; then
  echo "HTTP half harness: acceptance/at_r1_http.py as it is at $HARNESS_AT$([ "$COPIED_HARNESS" = 1 ] && echo ', copied into this checkout'), sha256 $(sha256sum < "$HARNESS" | cut -c1-64)" | tee -a "$OUT/commit.txt"
fi
if [ "$RUN_HTTP" = 0 ]; then
  say "HTTP half: not run (HALVES=$HALVES)"
elif [ -f "$HARNESS" ]; then
  say "HTTP half: python3 acceptance/at_r1_http.py --keep-going"
  set +e
  (cd "$W/openDox-code" && python3 acceptance/at_r1_http.py --keep-going) > "$OUT/http-half.log" 2>&1
  HTTP_RC=$?
  set -e
  tail -25 "$OUT/http-half.log"
  # the harness's own last line, less its leading verdict word and outer parentheses
  HTTP_LINE=$(sed -n 's/^AT-R1 HTTP half: //p' "$OUT/http-half.log" | tail -1 \
    | sed -e 's/^\(PASS\|FAIL\|ERROR\):\{0,1\} *//' -e 's/^(\(.*\))$/\1/')
  HTTP_LINE=${HTTP_LINE:-"no verdict line; exit $HTTP_RC"}
else
  HTTP_LINE="acceptance/at_r1_http.py is absent at this commit (T095 has not landed there)"
fi
if [ "$RUN_HTTP" = 1 ]; then
  echo "$HTTP_RC" > "$OUT/http-half.rc"
  say "HTTP half exit $HTTP_RC"
  git -C "$W/openDox-code" status --porcelain --ignored > "$OUT/tree-after-harness.txt"
  if [ "$COPIED_HARNESS" = 1 ]; then
    # the copy goes again, so the browser half installs the tree exactly as P has it
    if git -C "$W/openDox-code" cat-file -e "HEAD:acceptance/at_r1_http.py" 2>/dev/null; then
      git -C "$W/openDox-code" checkout -q -- acceptance/at_r1_http.py
    else
      rm -f "$HARNESS"
      rmdir "$W/openDox-code/acceptance" 2>/dev/null || true
    fi
    git -C "$W/openDox-code" status --porcelain --ignored > "$OUT/tree-after-harness-restored.txt"
    test ! -s "$OUT/tree-after-harness-restored.txt" || { say "FAIL: the checkout is not clean after the copied harness went"; exit 2; }
  else
    # the commit's own harness must leave its checkout exactly as it was, or
    # the browser half would install a tree other than the commit's
    # (Copilot r4186065384 on openxFactory#1241)
    test ! -s "$OUT/tree-after-harness.txt" || { say "FAIL: the harness left the checkout modified (tree-after-harness.txt)"; exit 2; }
  fi
fi
case " $HALVES " in *" browser "*) ;; *)
  if [ "$HTTP_RC" -eq 0 ]; then H=PASS; else H=FAIL; fi
  echo "AT-R1 HTTP half    at $P: $H ($HTTP_LINE)" | tee "$OUT/verdict.txt"
  exit "$HTTP_RC";;
esac

# ---- 2. the browser half: quickstart.md § 1 ---------------------------------
python3 -m venv --clear "$W/v"
# shellcheck disable=SC1091
. "$W/v/bin/activate"
# the README's stand-in until the cut, `pip install "./code[local]"` (T076, as #1225 amends it),
# CONSTRAINED BY THE SAME LOCK, ON THE SAME CONDITION, AS T095's HARNESS
# (`install_opendox`: the commit's constraints-cpython312-linux.txt, with a
# CPython 3.12 on Linux), so both halves measure one dependency set (the
# holder's ruling on t096-dry finding F3).
LOCK_ARGS=()
LOCK=$W/openDox-code/constraints-cpython312-linux.txt
if [ -f "$LOCK" ] && python3 -c 'import sys; sys.exit(0 if sys.platform.startswith("linux") and sys.implementation.name == "cpython" and sys.version_info[:2] == (3, 12) else 1)'; then
  LOCK_ARGS=(-c "$LOCK")
else
  say "NOTE: no lock applies here (absent, or not CPython 3.12 on Linux); the harness would also install unlocked"
fi
pip install -q --disable-pip-version-check "${LOCK_ARGS[@]}" "$W/openDox-code[local]"
echo "browser half install: pip install ${LOCK_ARGS[*]} <checkout>[local]" >> "$OUT/commit.txt"
pip list --format=freeze > "$OUT/venv-freeze.txt"
for s in openxdox ideation_dashboard doc_health corpus_adapter_openxfactory; do
  if python -c "import importlib.util, sys; sys.exit(0 if importlib.util.find_spec('$s') else 1)"; then say "FAIL: $s is importable"; exit 1; fi
done
if [ -n "$(command -v omp || true)" ]; then say "FAIL: a harness is installed, so no-model is not what this measures"; exit 1; fi
if [ -n "$(command -v openprofiler-broker || true)" ]; then say "FAIL: an identity broker is installed"; exit 1; fi
python3 - <<'PY'
import socket
for host in ("127.0.0.1", "::1"):
    try:
        s = socket.create_connection((host, 5432), timeout=1)
    except OSError:
        continue
    s.close()
    raise SystemExit(f"FAIL: a database already listens on {host}:5432")
print("no database listens on the default port")
PY
OPENDOX_STATE_DIR=$(mktemp -d)   # declared apart, so a failed mktemp stops the run (set -e)
export OPENDOX_STATE_DIR
test -z "$(ls -A "$OPENDOX_STATE_DIR")"
say "§ 1: openDox alone in $W/v; OPENDOX_STATE_DIR $OPENDOX_STATE_DIR"

# ---- § 2: two plain git repositories -----------------------------------------
A=$W/repos/plain-documents
mkdir -p "$W/repos"
cp -r "$W/openDox-code/tests/fixtures/plain-documents" "$A"
B=$W/repos/plain-notes
mkdir -p "$B"
printf '# Roadmap\n\nThe roadmap links to the [budget](budget.md) and the [notes](notes.md).\n' > "$B/roadmap.md"
printf '# Budget\n\nBudget figures for the roadmap.\n' > "$B/budget.md"
printf '# Meeting notes\n\nWe discussed the roadmap and the budget.\n' > "$B/notes.md"
for R in "$A" "$B"; do
  git -C "$R" init -q
  git -C "$R" config user.name fixture
  git -C "$R" config user.email fixture@example.invalid
  git -C "$R" add -A
  git -C "$R" commit -qm fixture
  if test -e "$R/ideation/dashboard/model-provider-bindings.yaml"; then say "FAIL: $R holds a model binding"; exit 1; fi
done

# ---- the Playwright driver's own venv (never the product's) -------------------
if [ -z "${DRV_PYTHON:-}" ]; then
  python3 -m venv "$W/drv"
  "$W/drv/bin/pip" install -q --disable-pip-version-check "playwright==${PLAYWRIGHT_VERSION:-1.63.0}" PyYAML
  # a shared cache may be read-only (a container's root-owned browser cache):
  # then the browser goes to the scratch space, and the drive reads it there
  if ! "$W/drv/bin/python" -m playwright install chromium > "$OUT/playwright-install.log" 2>&1; then
    export PLAYWRIGHT_BROWSERS_PATH=$W/ms-playwright
    say "NOTE: the browser cache cannot be written; installing Chromium into $PLAYWRIGHT_BROWSERS_PATH"
    "$W/drv/bin/python" -m playwright install chromium >> "$OUT/playwright-install.log" 2>&1
  fi
  DRV_PYTHON=$W/drv/bin/python
fi
"$DRV_PYTHON" -c 'import importlib.metadata as m; print("driver: playwright", m.version("playwright"))' | tee -a "$OUT/commit.txt"
echo "driver: PLAYWRIGHT_BROWSERS_PATH ${PLAYWRIGHT_BROWSERS_PATH:-unset (the default of playwright)}" | tee -a "$OUT/commit.txt"

# ---- §§ 3-5, once per repository -----------------------------------------------
browser_pass() {
  # Every check below fails the pass EXPLICITLY: this function runs in an
  # `||` list, where bash ignores `set -e`.
  local label=$1 R=$2 out=$OUT/$1 rc=0 token copy failed
  mkdir -p "$out"
  : > "$out/failed.txt"
  fail() { say "FAIL ($label): $*"; echo "$*" >> "$out/failed.txt"; stop_server; return 1; }
  python3 - "$PORT" <<'PY' || { fail "port $PORT is taken"; return 1; }
import socket, sys
port = int(sys.argv[1])
for host in ("127.0.0.1", "::1"):
    try:
        s = socket.create_connection((host, port), timeout=1)
    except OSError:
        continue
    s.close()
    raise SystemExit(f"FAIL: something already listens on {host}:{port}, so a ready answer would not come from this run")
PY
  mkdir -p "$W/run-cwd"
  # § 3: the one documented command (R1Q15 (b)), from outside the checkout
  (cd "$W/run-cwd" && exec opendox generate-and-open --local --repo-root "$R" --repository fixture --no-open --port "$PORT") \
    > "$out/server.stdout" 2> "$out/server.stderr" &
  SERVER=$!
  local ready=0
  for _ in $(seq 1 60); do
    kill -0 "$SERVER" 2>/dev/null || { tail -20 "$out/server.stderr"; SERVER=; fail "the server exited before it answered"; return 1; }
    if curl -sf -o /dev/null "http://127.0.0.1:$PORT/"; then ready=1; break; fi
    sleep 1
  done
  [ "$ready" -eq 1 ] || { fail "no answer in 60 s"; return 1; }
  kill -0 "$SERVER" || { fail "the started process is gone"; return 1; }   # the port was free before, so it is the one answering
  curl -sf "http://127.0.0.1:$PORT/" > "$out/index.html" && grep -qi '<html' "$out/index.html" || { fail "/ is not HTML"; return 1; }
  curl -sf "http://127.0.0.1:$PORT/snapshot.json" > "$out/snap.json" || { fail "/snapshot.json"; return 1; }
  curl -sf "http://127.0.0.1:$PORT/capabilities" > "$out/caps.json" || { fail "/capabilities"; return 1; }
  # the answering server is this run's: the snapshot's revision is this fixture's HEAD
  python3 - "$out/snap.json" "$(git -C "$R" rev-parse HEAD)" <<'PY' || { fail "the snapshot is not this run's"; return 1; }
import json, sys
got = (json.load(open(sys.argv[1])).get("generation") or {}).get("source_revision")
if got != sys.argv[2]:
    raise SystemExit(f"FAIL: snapshot source_revision {got} is not this fixture's HEAD {sys.argv[2]}")
PY
  copy=$OPENDOX_STATE_DIR/console/$PORT.html
  # T104's start prints the copy's location as ONE `console file://…` line
  # (`PrivateCopy.file_url`, `Path.as_uri()`), never the token. quickstart.md
  # § 4 step 1 opens exactly the URL the command printed, so it is read from
  # the start's output, and it must name the copy at the documented path.
  copy_url=$(python3 - "$out/server.stdout" "$copy" <<'PY'
import os, re, sys, urllib.parse
lines = open(sys.argv[1], encoding="utf-8", errors="replace").read().splitlines()
urls = [m.group(1) for m in (re.match(r"\s*console (file://\S+)", line) for line in lines) if m]
assert len(urls) == 1, f"the start printed {len(urls)} console file:// URL line(s), not one"
parts = urllib.parse.urlsplit(urls[0])
assert parts.scheme == "file" and parts.netloc in ("", "localhost") and not parts.query and not parts.fragment, "the printed console URL is not a plain file:// URL"
assert os.path.samefile(urllib.parse.unquote(parts.path), sys.argv[2]), "the printed console URL does not name OPENDOX_STATE_DIR/console/PORT.html"
print(urls[0])
PY
) || { fail "the start did not print the private copy's file:// URL"; return 1; }
  echo "$copy_url" > "$out/console-url.txt"
  # T104's B3 hint line (RULED 5982436447, item 1) is recorded, not judged here:
  # it is T104's own falsifier's, and quickstart.md does not name it
  if grep -q 'STATE_DIR to a folder that is not hidden' "$out/server.stdout"; then echo printed > "$out/b3-hint.txt"; else echo absent > "$out/b3-hint.txt"; fi
  # quickstart.md § 3 on main (T007 batch N): the token from the private copy, and
  # the RAW /capabilities payload carries it neither by name nor by value
  token=$(python3 - "$copy" "$PORT" "$out/caps.json" <<'PY'
import html, os, re, stat, sys, urllib.parse
copy, port, caps_path = sys.argv[1], int(sys.argv[2]), sys.argv[3]
for path, mode in ((os.path.dirname(copy), 0o700), (copy, 0o600)):
    info = os.lstat(path)
    assert info.st_uid == os.getuid() and stat.S_IMODE(info.st_mode) == mode, f"{path} is not this user's own, mode {mode:o}"
assert stat.S_ISREG(os.lstat(copy).st_mode), "the private copy is not a regular file"
text = open(copy).read()
assert all(m.start() > 0 and text[m.start() - 1] == "#" for m in re.finditer("console_token=", text)), "the private copy puts the token outside a fragment"
target = re.search(r"""(?i)http-equiv=["']?refresh["']?\s+content=["']\s*\d+\s*;\s*url=([^"']+)""", text)
assert target, "the private copy forwards to no page"
url = urllib.parse.urlsplit(html.unescape(target.group(1)))
assert (url.scheme, url.netloc, url.path, url.query) == ("http", f"127.0.0.1:{port}", "/index.html", ""), "the private copy does not forward to this server's /index.html with an empty query"
token = urllib.parse.parse_qs(url.fragment).get("console_token", [""])[0]
assert token, "the opened URL carries no token in its fragment"
caps_raw = open(caps_path).read()
assert "console_token" not in caps_raw and token not in caps_raw, "/capabilities carries the console token"
print(token)
PY
) || { fail "the private copy"; return 1; }
  # the header goes over stdin, never onto curl's command line, which every user of the machine can read, as quickstart § 3 sends it
  printf 'X-XF-Console-Token: %s\n' "$token" | curl -sf -H @- "http://127.0.0.1:$PORT/workbench/model-catalog" > "$out/catalog.json" \
    || { fail "the model catalog with the copy's token"; return 1; }
  python3 - "$out/snap.json" "$out/caps.json" "$out/catalog.json" > "$out/http-checks.txt" <<'PY' || { cat "$out/http-checks.txt"; fail "quickstart § 3's checks"; return 1; }
import json, sys
snap, caps, cat = (json.load(open(p)) for p in sys.argv[1:4])
assert snap.get("documents"), "the snapshot is empty"
assert (caps.get("install") or {}).get("mode") == "local", caps.get("install")
assert "console_token" not in caps, "/capabilities still carries the console token"
available = [m["model_id"] for m in cat["models"] if m["available"]]   # xfactory-workbench-model-catalog
assert not available, f"no model is configured, yet the catalog offers {available}"
print("quickstart § 3: bundle, neutral snapshot, local mode, no token on /capabilities, and an empty catalog")
PY
  cat "$out/http-checks.txt"
  # § 4: the browser half
  "$DRV_PYTHON" "$DRIVER" --port "$PORT" --label "$label" --out "$out" --odc "$W/openDox-code" --copy "$copy" \
    --copy-url "$copy_url" > "$out/driver.log" 2>&1 || rc=$?
  tail -45 "$out/driver.log"
  failed=$(sed -n 's/^FAILED CHECKS: //p' "$out/driver.log" | tail -1)
  case "$failed" in "[]") ;; "") echo "the driver reached no verdict (exit $rc)" >> "$out/failed.txt";; *) echo "$failed" >> "$out/failed.txt";; esac
  # § 5: tear down
  stop_server
  sleep 2
  if [ -e "$copy" ]; then say "FAIL ($label): the private copy outlived the server"; echo "the private copy outlived the server" >> "$out/failed.txt"; rc=1; fi
  if ps -eo args | grep -F "$OPENDOX_STATE_DIR" | grep -v grep > "$out/leftover.txt"; then
    say "FAIL ($label): processes left referencing the state directory (R1Q16 (iv))"; cat "$out/leftover.txt"
    echo "processes left referencing the state directory" >> "$out/failed.txt"; rc=1
  fi
  if grep -qF 'console_token=' "$out/server.stdout" "$out/server.stderr"; then say "FAIL ($label): the start printed the token"; echo "the start printed the token" >> "$out/failed.txt"; rc=1; fi
  # and no file of this pass's record holds the token's VALUE: the record is
  # committed as evidence. The value goes to grep over stdin, never argv.
  # grep's own status is read: 1 is clean, 0 a match, anything else no answer.
  printf '%s\n' "$token" | grep -rqF -f - "$out"; local leak=${PIPESTATUS[1]}
  case "$leak" in
    1) echo "no file of this pass's record holds the token's value" > "$out/token-scan.txt";;
    0) say "FAIL ($label): the record holds the console token's value"; echo "the record holds the console token's value" >> "$out/failed.txt"; rc=1;;
    *) say "FAIL ($label): the token scan gave no answer (grep exit $leak)"; echo "the token scan gave no answer" >> "$out/failed.txt"; rc=1;;
  esac
  echo "$rc" > "$out/browser.rc"
  say "browser half ($label) exit $rc"
  return "$rc"
}
BA=0; BB=0
browser_pass a "$A" || BA=$?
browser_pass b "$B" || BB=$?

# ---- the record: one verdict line per half ---------------------------------------
pass_word() {   # <label> <rc>
  if [ "$2" -eq 0 ]; then echo "($1) PASS"; else echo "($1) FAIL $(paste -sd ';' "$OUT/$1/failed.txt" 2>/dev/null)"; fi
}
if [ "$BA" -eq 0 ] && [ "$BB" -eq 0 ]; then BW=PASS; else BW=FAIL; fi
if [ "$HTTP_RC" -eq 0 ]; then HW=PASS; else HW=FAIL; fi
{
  if [ "$RUN_HTTP" = 1 ]; then echo "AT-R1 HTTP half    at $P: $HW ($HTTP_LINE)"; fi
  echo "AT-R1 browser half at $P: $BW ($(pass_word a "$BA"); $(pass_word b "$BB"))"
} | tee "$OUT/verdict.txt"
echo "finished $(date -u +%FT%TZ)" >> "$OUT/commit.txt"
rm -rf "$OPENDOX_STATE_DIR"
[ "$BA" -eq 0 ] && [ "$BB" -eq 0 ] && { [ "$RUN_HTTP" = 0 ] || [ "$HTTP_RC" -eq 0 ]; }
