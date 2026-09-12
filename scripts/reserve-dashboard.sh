#!/usr/bin/env bash
# reserve-dashboard.sh — bring the ideation dashboard's local plane up, idempotently.
#
# WHY THIS EXISTS. The multi-repository serve was started by hand, as a `nohup`
# with a fourteen-argument list, against a plane living in a per-session `/tmp`
# scratchpad. Two power cuts in two days (2026-08-12, 2026-08-13) killed it both
# times, and each recovery depended on an argv file that happened to survive in a
# dead session's scratchpad. Neither the argv nor the plane belonged in /tmp.
#
# So: the plane gets a durable home under XDG state, the argument list is DERIVED
# rather than remembered, and bringing the dashboard back is one command that is
# safe to run when it is already up.
#
#   reserve-dashboard.sh              ensure the plane, then serve (foreground)
#   reserve-dashboard.sh --status     say whether it is up, exit 0/1
#   reserve-dashboard.sh --rebuild    republish every registered repository first
#   reserve-dashboard.sh --supervise  restart the serve if it dies (see NOTE)
#   reserve-dashboard.sh --stop       stop the serve listening on this port
#
# NOTE ON SUPERVISION. `--supervise` exists because this host runs WSL2 with
# `systemd=false` in /etc/wsl.conf, so `systemctl --user` cannot run and the
# accompanying systemd unit is inert until systemd is enabled. Supervision here
# is a restart loop in one process, not a service manager: it survives a crash,
# NOT a reboot. Boot-start options are documented beside the unit file.
#
# Env overrides: XF_DASHBOARD_PORT, XF_DASHBOARD_PLANE, XF_DASHBOARD_ACTOR.

set -euo pipefail

PORT="${XF_DASHBOARD_PORT:-8765}"
PLANE="${XF_DASHBOARD_PLANE:-${XDG_STATE_HOME:-$HOME/.local/state}/xfactory-dashboard/local-plane}"

# The serving checkout is the repository this script lives in — never a guess and
# never a saved path, so a copy of the runtime in another worktree serves ITSELF.
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# The aggregation checkout is the nearest ancestor carrying the project register.
# That file is what the serve needs anyway, so finding it and finding the
# aggregation root are the same question.
find_aggregation_root() {
  local dir="$REPO_ROOT"
  while [ "$dir" != "/" ]; do
    if [ -f "$dir/project-register.yaml" ]; then printf '%s\n' "$dir"; return 0; fi
    dir="$(dirname "$dir")"
  done
  return 1
}

AGG_ROOT="$(find_aggregation_root)" || {
  echo "reserve-dashboard: no project-register.yaml above $REPO_ROOT — cannot locate" \
       "the aggregation checkout, so the register and the member roots are unknown." >&2
  exit 2
}
ACTOR="${XF_DASHBOARD_ACTOR:-$(git -C "$REPO_ROOT" config user.name || echo "$USER")}"
INDEX="$PLANE/index.json"

is_up() { curl -sf -o /dev/null --max-time 3 "http://127.0.0.1:$PORT/capabilities"; }

listening_pid() {
  # The serve process holding the port, or empty. Never `pgrep -f serve` — that
  # pattern matches the shell running the pgrep (it bit this project twice).
  ss -ltnp 2>/dev/null | awk -v p=":$PORT\$" '$4 ~ p' \
    | grep -oE 'pid=[0-9]+' | cut -d= -f2 | head -1
}

build_plane() {
  echo "reserve-dashboard: publishing every registered repository into $PLANE"
  mkdir -p "$PLANE"
  ( cd "$REPO_ROOT" && PYTHONPATH=scripts python3 -m ideation_dashboard.nightly_lane \
      --repo-root "$AGG_ROOT" --repositories registered --out-dir "$PLANE" )
}

# `--source-root` is per entry and fail-closed: an entry with no declared root
# serves no documents. Derive one per PUBLISHED repository from the index the lane
# just wrote, so the serve can never disagree with the plane about who is in it.
# openxFactory resolves to the SERVING checkout, because that is the tree the gate
# acts on; every other id resolves under the aggregation layout.
source_root_args() {
  python3 - "$INDEX" "$AGG_ROOT" "$REPO_ROOT" <<'PY'
import json, sys, os
index, agg, repo_root = sys.argv[1], sys.argv[2], sys.argv[3]
with open(index) as fh:
    entries = json.load(fh).get("entries") or []
out, unresolved = [], []
for entry in entries:
    rid = entry.get("repository")
    if not rid:
        continue
    if rid == "openxFactory":
        out.append(f"{rid}={repo_root}")
        continue
    for candidate in (os.path.join(agg, "xFactories", rid),
                      os.path.join(agg, "installs", rid)):
        if os.path.isdir(candidate):
            out.append(f"{rid}={candidate}")
            break
    else:
        unresolved.append(rid)
for pair in out:
    print("--source-root"); print(pair)
if unresolved:
    print("# unresolved: " + ",".join(unresolved), file=sys.stderr)
PY
}

serve_argv() {
  local snapshot="$PLANE/openxFactory-snapshot.json"
  printf '%s\n' \
    --snapshot "$snapshot" \
    --checkout-root "$REPO_ROOT" \
    --local-index "$INDEX" \
    --repository openxFactory \
    --actor "$ACTOR" \
    --port "$PORT" \
    --project-register "$AGG_ROOT/project-register.yaml"
  source_root_args
}

exec_serve() {
  local -a argv=()
  while IFS= read -r line; do argv+=("$line"); done < <(serve_argv)
  echo "reserve-dashboard: serving $REPO_ROOT on http://127.0.0.1:$PORT" \
       "(${#argv[@]} args, actor $ACTOR)"
  cd "$REPO_ROOT"
  # THROUGH THIS REPOSITORY'S OWN ENTRYPOINT, not `-m` on the package
  # (`split-opendox-two-layer-product` § 5.2, RULED (a) POST-SHED MODE, `#656`
  # `5625573095`). `ideation_dashboard.serve` left for openDox-code in the shed;
  # the wrapper reads it through this repository's PIN, puts BOTH legs' `src/`
  # on the path — the serve's columns span openDox and openXdox — and makes the
  # ONE process-start registration `build_server`'s lazy profile proxy resolves
  # through. See `scripts/ideation-dashboard-serve.py`'s docstring for why
  # the one old line cannot be re-pointed in place.
  exec python3 scripts/ideation-dashboard-serve.py "${argv[@]}"
}

ensure_plane() {
  if [ ! -f "$INDEX" ]; then
    echo "reserve-dashboard: no plane at $PLANE — building it"
    build_plane
  fi
}

case "${1:-}" in
  --status)
    if is_up; then
      pid="$(listening_pid)"
      echo "up on http://127.0.0.1:$PORT (pid ${pid:-unknown}, plane $PLANE)"
      exit 0
    fi
    echo "down (nothing answering /capabilities on port $PORT)"; exit 1
    ;;
  --stop)
    pid="$(listening_pid)"
    if [ -z "$pid" ]; then echo "reserve-dashboard: nothing listening on $PORT"; exit 0; fi
    echo "reserve-dashboard: stopping pid $pid"; kill "$pid"
    for _ in $(seq 1 10); do kill -0 "$pid" 2>/dev/null || { echo "stopped"; exit 0; }; sleep 1; done
    echo "reserve-dashboard: pid $pid did not stop" >&2; exit 1
    ;;
  --rebuild)
    if is_up; then
      echo "reserve-dashboard: already up on port $PORT — stop it first to rebuild" >&2
      exit 1
    fi
    build_plane; exec_serve
    ;;
  --supervise)
    ensure_plane
    # Restart on crash only. A reboot needs a boot-time starter; see the unit file.
    while true; do
      if is_up; then sleep 10; continue; fi
      ( exec_serve ) || true
      echo "reserve-dashboard: serve exited — restarting in 2s" >&2
      sleep 2
    done
    ;;
  ""|--serve)
    if is_up; then
      echo "reserve-dashboard: already up on http://127.0.0.1:$PORT (pid $(listening_pid)) — nothing to do"
      exit 0
    fi
    ensure_plane; exec_serve
    ;;
  -h|--help)
    sed -n '2,30p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'; exit 0
    ;;
  *)
    echo "reserve-dashboard: unknown option $1 (try --help)" >&2; exit 2
    ;;
esac
