#!/usr/bin/env bash

set -euo pipefail

JSON_MODE=false
if [ "${1:-}" = "--json" ]; then
    JSON_MODE=true
fi

SCRIPT_DIR="$(CDPATH="" cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCRIPT_REPO_ROOT="$(CDPATH="" cd "$SCRIPT_DIR/../../../../.." && pwd)"

trim() {
    local value="$1"
    value="${value#"${value%%[![:space:]]*}"}"
    value="${value%"${value##*[![:space:]]}"}"
    printf '%s' "$value"
}

resolve_config_value() {
    local repo_root="$1"
    local key="$2"
    local default_value="$3"
    local config_file="$repo_root/.specify/extensions/git/git-config.yml"

    if [ ! -f "$config_file" ]; then
        printf '%s\n' "$default_value"
        return 0
    fi

    local raw_value
    raw_value=$(awk -F':' -v key="$key" '$1 == key {sub(/^[^:]*:[[:space:]]*/, "", $0); print $0; exit}' "$config_file")
    raw_value=$(trim "${raw_value:-}")
    if [ -z "$raw_value" ]; then
        printf '%s\n' "$default_value"
    else
        printf '%s\n' "$raw_value"
    fi
}

resolve_path_from_root() {
    local repo_root="$1"
    local raw_path="$2"
    local combined

    if [[ "$raw_path" = /* ]]; then
        combined="$raw_path"
    else
        combined="$repo_root/$raw_path"
    fi

    local parent_dir
    parent_dir=$(dirname "$combined")
    local leaf_name
    leaf_name=$(basename "$combined")
    if [ -d "$parent_dir" ]; then
        printf '%s/%s\n' "$(cd "$parent_dir" && pwd -P)" "$leaf_name"
    else
        printf '%s\n' "$combined"
    fi
}

resolve_main_repo_root() {
    local repo_root="$1"

    local inferred_root
    case "$repo_root" in
        */.worktrees/*)
            inferred_root="${repo_root%%/.worktrees/*}"
            if [ -d "$inferred_root/.specify" ]; then
                (cd "$inferred_root" && pwd -P)
                return 0
            fi
            ;;
        */worktrees/*)
            inferred_root="${repo_root%%/worktrees/*}"
            if [ -d "$inferred_root/.specify" ]; then
                (cd "$inferred_root" && pwd -P)
                return 0
            fi
            ;;
    esac

    local worktree_parent
    worktree_parent=$(dirname "$repo_root")
    local worktree_parent_name
    worktree_parent_name=$(basename "$worktree_parent")
    if [[ "$worktree_parent_name" == *-worktrees ]]; then
        inferred_root="$(dirname "$worktree_parent")/${worktree_parent_name%-worktrees}"
        if [ -d "$inferred_root/.specify" ]; then
            (cd "$inferred_root" && pwd -P)
            return 0
        fi
    fi

    local common_dir
    common_dir=$(git -C "$repo_root" rev-parse --git-common-dir 2>/dev/null || true)

    if [ -z "$common_dir" ]; then
        printf '%s\n' "$repo_root"
        return 0
    fi

    if [[ "$common_dir" != /* ]]; then
        common_dir="$repo_root/$common_dir"
    fi

    if [ "$(basename "$common_dir")" = ".git" ]; then
        local main_root
        main_root=$(dirname "$common_dir")
        if [ -d "$main_root" ]; then
            (cd "$main_root" && pwd -P)
            return 0
        fi
    fi

    printf '%s\n' "$repo_root"
}

worktree_root_has_entries() {
    local candidate="$1"
    local first

    [ -d "$candidate" ] || return 1
    first=$(find "$candidate" -maxdepth 1 -mindepth 1 -type d -print -quit 2>/dev/null || true)
    [ -n "$first" ]
}

resolve_worktree_root() {
    local repo_root="$1"
    local main_root
    main_root=$(resolve_main_repo_root "$repo_root")

    local candidate
    for candidate in "$(resolve_path_from_root "$main_root" "worktrees")" "$(resolve_path_from_root "$main_root" ".worktrees")"; do
        if worktree_root_has_entries "$candidate"; then
            (cd "$candidate" && pwd -P)
            return 0
        fi
    done

    local default_root="../$(basename "$main_root")-worktrees"
    local raw_root
    raw_root=$(resolve_config_value "$main_root" "worktree_root" "$default_root")
    candidate=$(resolve_path_from_root "$main_root" "$raw_root")
    printf '%s\n' "$candidate"
}

canonicalize_if_dir() {
    local candidate="$1"
    if [ -d "$candidate" ]; then
        (cd "$candidate" && pwd -P)
    else
        printf '%s\n' "$candidate"
    fi
}

emit_result() {
    local branch_name="$1"
    local worktree_path="$2"
    local base_branch="$3"
    local repo_root="$4"
    local source="$5"

    if $JSON_MODE; then
        if command -v jq >/dev/null 2>&1; then
            jq -cn \
                --arg branch_name "$branch_name" \
                --arg worktree_path "$worktree_path" \
                --arg base_branch "$base_branch" \
                --arg repo_root "$repo_root" \
                --arg source "$source" \
                '{BRANCH_NAME:$branch_name,WORKTREE_PATH:$worktree_path,BASE_BRANCH:$base_branch,REPO_ROOT:$repo_root,SOURCE:$source}'
        elif command -v python3 >/dev/null 2>&1; then
            python3 - "$branch_name" "$worktree_path" "$base_branch" "$repo_root" "$source" <<'PY'
import json
import sys

print(json.dumps({
    "BRANCH_NAME": sys.argv[1],
    "WORKTREE_PATH": sys.argv[2],
    "BASE_BRANCH": sys.argv[3],
    "REPO_ROOT": sys.argv[4],
    "SOURCE": sys.argv[5],
}))
PY
        else
            printf '{"BRANCH_NAME":"%s","WORKTREE_PATH":"%s","BASE_BRANCH":"%s","REPO_ROOT":"%s","SOURCE":"%s"}\n' \
                "$branch_name" "$worktree_path" "$base_branch" "$repo_root" "$source"
        fi
    else
        printf '%s\n' "$worktree_path"
    fi
}

REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null || true)
if [ -z "$REPO_ROOT" ]; then
    REPO_ROOT="$SCRIPT_REPO_ROOT"
fi
if [ -z "$REPO_ROOT" ] || [ ! -d "$REPO_ROOT/.specify" ]; then
    echo "Error: not inside a Git repository or Speckit checkout." >&2
    exit 1
fi

COMMON_DIR=$(git rev-parse --git-common-dir 2>/dev/null || true)
if [ -z "$COMMON_DIR" ]; then
    MAIN_REPO_ROOT=$(resolve_main_repo_root "$REPO_ROOT")
    COMMON_DIR="$MAIN_REPO_ROOT/.git"
fi
if [[ "$COMMON_DIR" != /* ]]; then
    COMMON_DIR="$REPO_ROOT/$COMMON_DIR"
fi

STATE_FILE="$COMMON_DIR/speckit-last-worktree.json"
BASE_BRANCH=$(resolve_config_value "$REPO_ROOT" "base_branch" "main")

if [ -f "$STATE_FILE" ]; then
    WORKTREE_PATH=""
    BRANCH_NAME=""
    if command -v jq >/dev/null 2>&1; then
        WORKTREE_PATH=$(jq -r '.WORKTREE_PATH // ""' "$STATE_FILE")
        BRANCH_NAME=$(jq -r '.BRANCH_NAME // ""' "$STATE_FILE")
    elif command -v python3 >/dev/null 2>&1; then
        WORKTREE_PATH=$(python3 - "$STATE_FILE" <<'PY'
import json
import sys

with open(sys.argv[1], "r", encoding="utf-8") as fh:
    print(json.load(fh).get("WORKTREE_PATH", ""))
PY
)
        BRANCH_NAME=$(python3 - "$STATE_FILE" <<'PY'
import json
import sys

with open(sys.argv[1], "r", encoding="utf-8") as fh:
    print(json.load(fh).get("BRANCH_NAME", ""))
PY
)
    else
        WORKTREE_PATH=$(grep -o '"WORKTREE_PATH"[[:space:]]*:[[:space:]]*"[^"]*"' "$STATE_FILE" | sed 's/.*"\([^"]*\)"$/\1/')
        BRANCH_NAME=$(grep -o '"BRANCH_NAME"[[:space:]]*:[[:space:]]*"[^"]*"' "$STATE_FILE" | sed 's/.*"\([^"]*\)"$/\1/')
    fi

    if [ -n "$WORKTREE_PATH" ] && [ -d "$WORKTREE_PATH" ]; then
        WORKTREE_PATH=$(canonicalize_if_dir "$WORKTREE_PATH")
        emit_result "$BRANCH_NAME" "$WORKTREE_PATH" "$BASE_BRANCH" "$REPO_ROOT" "state_file"
        exit 0
    fi
fi

WORKTREE_ROOT=$(resolve_worktree_root "$REPO_ROOT")
LATEST_WORKTREE=""
if [ -d "$WORKTREE_ROOT" ]; then
    LATEST_WORKTREE=$(find "$WORKTREE_ROOT" -maxdepth 1 -mindepth 1 -type d -printf '%T@ %p\n' 2>/dev/null | sort -nr | awk 'NR == 1 {print $2}')
fi

if [ -n "$LATEST_WORKTREE" ] && [ -d "$LATEST_WORKTREE" ]; then
    LATEST_WORKTREE=$(canonicalize_if_dir "$LATEST_WORKTREE")
    emit_result "$(basename "$LATEST_WORKTREE")" "$LATEST_WORKTREE" "$BASE_BRANCH" "$REPO_ROOT" "worktree_root_fallback"
    exit 0
fi

echo "Error: no Speckit worktree handoff has been recorded yet." >&2
exit 1
