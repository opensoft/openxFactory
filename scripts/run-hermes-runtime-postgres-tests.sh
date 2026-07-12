#!/bin/sh
set -eu

repo_root=$(CDPATH='' cd -- "$(dirname -- "$0")/.." && pwd)
compose_file="$repo_root/tests/hermes_runtime_contracts/postgres/compose.yaml"
lock_file="$repo_root/tests/hermes_runtime_contracts/postgres/images.lock.yaml"
evidence_dir="$repo_root/tests/hermes_runtime_contracts/postgres/evidence"
fixture_index="$repo_root/contracts/hermes-runtime/fixtures/index.yaml"

major=""
json_output=false
update_lock=false

usage() {
  printf '%s\n' 'usage: run-hermes-runtime-postgres-tests.sh [--major 15|16] [--json]' \
    '       run-hermes-runtime-postgres-tests.sh --update-image-lock'
}

while [ "$#" -gt 0 ]; do
  case "$1" in
    --major)
      [ "$#" -ge 2 ] || { usage >&2; exit 2; }
      major=$2
      shift 2
      ;;
    --json)
      json_output=true
      shift
      ;;
    --update-image-lock)
      update_lock=true
      shift
      ;;
    --help|-h)
      usage
      exit 0
      ;;
    *)
      usage >&2
      exit 2
      ;;
  esac
done

if [ -n "$major" ] && [ "$major" != 15 ] && [ "$major" != 16 ]; then
  printf '%s\n' 'unsupported PostgreSQL major; expected 15 or 16' >&2
  exit 2
fi

if [ "$update_lock" = true ] && { [ -n "$major" ] || [ "$json_output" = true ]; }; then
  printf '%s\n' '--update-image-lock cannot be combined with run options' >&2
  exit 2
fi

# A prior pass must never survive a new attempt.  Invalidate selected evidence
# before checking local dependencies, image availability, or Docker health.
if [ "$update_lock" = false ]; then
  if [ -n "$major" ]; then
    rm -f -- "$evidence_dir/postgres-$major.json"
  else
    rm -f -- "$evidence_dir/postgres-15.json" "$evidence_dir/postgres-16.json"
  fi
fi

if ! { [ -f "$compose_file" ] && [ -f "$lock_file" ] && [ -f "$fixture_index" ]; }; then
  printf '%s\n' 'PostgreSQL Compose definition or image lock is unavailable' >&2
  exit 2
fi

python_bin=python3
command -v "$python_bin" >/dev/null 2>&1 || {
  printf '%s\n' 'Python 3 is required for ephemeral credential generation' >&2
  exit 2
}
command -v docker >/dev/null 2>&1 || {
  printf '%s\n' 'Docker is required for PostgreSQL conformance' >&2
  exit 2
}

lookup_field() {
  awk -v wanted="$1" -v field="$2" '
    {
      key = $1
      gsub(/[\047":]/, "", key)
    }
    key == wanted && $1 ~ /:$/ { selected = 1; next }
    selected && $1 ~ /^[\047"]?[0-9]+[\047"]?:$/ { exit }
    selected && $1 == field ":" { print $2; exit }
  ' "$lock_file"
}

lookup_image() {
  lookup_field "$1" resolved_image
}

if [ "$update_lock" = true ]; then
  if [ "${HERMES_RUNTIME_CANDIDATE_FROZEN:-}" = 1 ]; then
    printf '%s\n' 'image-lock refresh is forbidden after candidate freeze' >&2
    exit 2
  fi
  digest_15=""
  digest_16=""
  for update_major in 15 16; do
    source_tag=$(lookup_field "$update_major" source_tag)
    [ "$source_tag" = "postgres:$update_major" ] || {
      printf '%s\n' "invalid official source tag for PostgreSQL $update_major" >&2
      exit 2
    }
    docker pull --platform linux/amd64 "$source_tag" >/dev/null
    resolved=$(docker image inspect --format '{{index .RepoDigests 0}}' "$source_tag")
    case "$resolved" in
      postgres@sha256:????????????????????????????????????????????????????????????????) ;;
      *)
        printf '%s\n' "Docker returned an invalid digest for PostgreSQL $update_major" >&2
        exit 2
        ;;
    esac
    if [ "$update_major" = 15 ]; then
      digest_15=$resolved
    else
      digest_16=$resolved
    fi
  done
  "$python_bin" -c 'import datetime, pathlib, sys, yaml
path = pathlib.Path(sys.argv[1])
document = yaml.safe_load(path.read_text(encoding="utf-8"))
resolved_at = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
for major, digest in (("15", sys.argv[2]), ("16", sys.argv[3])):
    entry = document["images"][major]
    entry["resolved_image"] = digest
    entry["update_evidence"] = {
        "resolved_at": resolved_at,
        "registry": "registry-1.docker.io/library/postgres",
        "media_type": "application/vnd.oci.image.index.v1+json",
        "command": f"docker pull --platform linux/amd64 postgres:{major}",
    }
temporary = path.with_suffix(path.suffix + ".tmp")
temporary.write_text(yaml.safe_dump(document, sort_keys=False), encoding="utf-8")
temporary.replace(path)' "$lock_file" "$digest_15" "$digest_16"
  printf '%s\n' 'updated PostgreSQL 15/16 image lock; review before candidate freeze'
  exit 0
fi

redact_log() {
  "$python_bin" -c 'import os, pathlib, sys
value = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8", errors="replace")
secret = os.environ.get("POSTGRES_PASSWORD", "")
sys.stdout.write(value.replace(secret, "<redacted>") if secret else value)' "$1"
}

run_one() {
  run_major=$1
  POSTGRES_IMAGE=$(lookup_image "$run_major")
  case "$POSTGRES_IMAGE" in
    postgres@sha256:????????????????????????????????????????????????????????????????) ;;
    *)
      printf '%s\n' "invalid or missing digest pin for PostgreSQL $run_major" >&2
      return 2
      ;;
  esac

  POSTGRES_PASSWORD=$(
    "$python_bin" -c 'import secrets; print(secrets.token_urlsafe(36))'
  )
  COMPOSE_PROJECT_NAME="hcs-$run_major-$$-$($python_bin -c 'import secrets; print(secrets.token_hex(5))')"
  export POSTGRES_IMAGE POSTGRES_PASSWORD COMPOSE_PROJECT_NAME
  raw_log=$(mktemp "${TMPDIR:-/tmp}/hcs-postgres.XXXXXX")
  junit_file=$(mktemp "${TMPDIR:-/tmp}/hcs-postgres-junit.XXXXXX")
  evidence_temporary=""

  cleanup() {
    if [ -n "${COMPOSE_PROJECT_NAME:-}" ]; then
      docker compose --file "$compose_file" --project-name "$COMPOSE_PROJECT_NAME" \
        down --volumes --remove-orphans >"$raw_log" 2>&1 || true
    fi
    rm -f -- "$raw_log" "$junit_file"
    if [ -n "${evidence_temporary:-}" ]; then
      rm -f -- "$evidence_temporary"
    fi
    unset POSTGRES_PASSWORD POSTGRES_IMAGE COMPOSE_PROJECT_NAME
  }
  trap cleanup EXIT HUP INT TERM

  if ! docker image inspect "$POSTGRES_IMAGE" >"$raw_log" 2>&1; then
    redact_log "$raw_log" >&2
    return 2
  fi
  if ! docker compose --file "$compose_file" --project-name "$COMPOSE_PROJECT_NAME" \
    up --detach --wait postgres >"$raw_log" 2>&1; then
    redact_log "$raw_log" >&2
    return 1
  fi
  if ! docker compose --file "$compose_file" --project-name "$COMPOSE_PROJECT_NAME" \
    run --rm psql-client >"$raw_log" 2>&1; then
    redact_log "$raw_log" >&2
    return 1
  fi

  if [ -x "$repo_root/.venv/bin/pytest" ]; then
    pytest_bin=$repo_root/.venv/bin/pytest
  elif command -v pytest >/dev/null 2>&1; then
    pytest_bin=$(command -v pytest)
  else
    printf '%s\n' 'pytest is required for PostgreSQL conformance' >&2
    return 2
  fi
  if ! HERMES_RUNTIME_POSTGRES_MAJOR=$run_major \
    PYTEST_ADDOPTS='' \
    PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONHASHSEED=0 \
    PYTHONPATH="$repo_root${PYTHONPATH:+:$PYTHONPATH}" \
    "$pytest_bin" -p no:cacheprovider --color=no -q \
      "$repo_root/tests/hermes_runtime_contracts/postgres" \
      -m postgres --junitxml="$junit_file" >"$raw_log" 2>&1; then
    redact_log "$raw_log" >&2
    return 1
  fi

  if ! test_count=$(
    "$python_bin" -c 'import pathlib, sys, xml.etree.ElementTree as ET
path = pathlib.Path(sys.argv[1])
root = ET.parse(path).getroot()
suites = [root] if root.tag == "testsuite" else list(root.findall("testsuite"))
tests = int(root.attrib.get("tests", sum(int(item.attrib.get("tests", 0)) for item in suites)))
failures = int(root.attrib.get("failures", sum(int(item.attrib.get("failures", 0)) for item in suites)))
errors = int(root.attrib.get("errors", sum(int(item.attrib.get("errors", 0)) for item in suites)))
skipped = int(root.attrib.get("skipped", sum(int(item.attrib.get("skipped", 0)) for item in suites)))
if tests < 1 or failures or errors or skipped:
    raise SystemExit(1)
print(tests)' "$junit_file"
  ); then
    printf '%s\n' 'pytest JUnit evidence is missing, empty, failed, or skipped' >&2
    return 1
  fi

  mkdir -p -- "$evidence_dir"
  evidence_file="$evidence_dir/postgres-$run_major.json"
  if ! evidence_json=$(
    PYTHONPATH="$repo_root${PYTHONPATH:+:$PYTHONPATH}" \
    "$python_bin" -c 'import json, pathlib, sys
from scripts.hermes_runtime_validation.fixtures import database_matrix_identity, repository_source_identity
from scripts.hermes_runtime_validation.loader import load_yaml_document
repo = pathlib.Path(sys.argv[1])
index = load_yaml_document(sys.argv[2])
major = int(sys.argv[3])
image = sys.argv[4]
test_count = int(sys.argv[5])
cases = [case for case in index["cases"] if case.get("phase") == "database" and major in case.get("database", {}).get("supported_majors", [])]
if len(cases) != 1:
    raise SystemExit(1)
case = cases[0]
record = {
    "schema_version": 1,
    "kind": "HermesRuntimePostgresEvidence",
    "major": major,
    "outcome": "pass",
    "image": image,
    "source_identity": repository_source_identity(repo, case),
    "suite": {"id": "hermes-runtime-postgres", "test_count": test_count},
    "matrix": database_matrix_identity(case),
}
print(json.dumps(record, ensure_ascii=False, sort_keys=True, separators=(",", ":")))' \
      "$repo_root" "$fixture_index" "$run_major" "$POSTGRES_IMAGE" "$test_count"
  ); then
    printf '%s\n' 'failed to derive deterministic PostgreSQL evidence identity' >&2
    return 1
  fi
  evidence_temporary=$(mktemp "$evidence_dir/.postgres-$run_major.XXXXXX")
  printf '%s\n' "$evidence_json" >"$evidence_temporary"
  mv -f -- "$evidence_temporary" "$evidence_file"
  evidence_temporary=""
  if [ "$json_output" = true ]; then
    printf '%s\n' "$evidence_json"
  else
    printf 'PostgreSQL %s conformance: pass (%s)\n' "$run_major" "$POSTGRES_IMAGE"
  fi

  trap - EXIT HUP INT TERM
  cleanup
}

if [ -n "$major" ]; then
  run_one "$major"
else
  run_one 15
  run_one 16
fi
