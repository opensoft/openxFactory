#!/bin/sh
# Session-locked v1-to-v2 migration runner (Hermes customer-subject runtime).
#
# One long-lived psql session, connected as a migrator-class login through the
# HERMES_MIGRATION_PSQL_COMMAND template, drives the whole governed protocol:
#
#   acquire the installation+migration session advisory lock
#     -> transaction: stage_migration + begin_migration_attempt   (STARTED
#        survives; a terminal prior success returns the stored result)
#     -> SERIALIZABLE transaction: execute_v1_cutover + commit
#     -> on cutover error: rollback, then fail_migration_attempt
#     -> release the lock
#
# Environment:
#   HERMES_MIGRATION_PSQL_COMMAND  psql command template. It is split on
#       whitespace (no embedded quoting) and must contain the literal
#       placeholder {database}, which is substituted with --database.
#       The connection must authenticate as a migrator-class login.
#
# Arguments:
#   --database <name> --staging-file <canonical-json path>
#   --installation-id <id> --migration-id <id>
#
# Exit codes: 0 success or converged terminal success; 1 migration failed or
# was rejected (FAILED/ABANDONED recorded when an attempt was open); 2 harness
# error (bad invocation, unreadable input, connection failure).

set -eu

usage() {
  printf 'usage: %s --database <name> --staging-file <path> ' "$0" >&2
  printf -- '--installation-id <id> --migration-id <id>\n' >&2
}

fail_harness() {
  printf 'hermes-v1-to-v2: harness-error: %s\n' "$1" >&2
  exit 2
}

database=''
staging_file=''
installation_id=''
migration_id=''

while [ "$#" -gt 0 ]; do
  case "$1" in
    --database)
      [ "$#" -ge 2 ] || { usage; exit 2; }
      database=$2
      shift 2
      ;;
    --staging-file)
      [ "$#" -ge 2 ] || { usage; exit 2; }
      staging_file=$2
      shift 2
      ;;
    --installation-id)
      [ "$#" -ge 2 ] || { usage; exit 2; }
      installation_id=$2
      shift 2
      ;;
    --migration-id)
      [ "$#" -ge 2 ] || { usage; exit 2; }
      migration_id=$2
      shift 2
      ;;
    *)
      usage
      exit 2
      ;;
  esac
done

[ -n "$database" ] || { usage; exit 2; }
[ -n "$staging_file" ] || { usage; exit 2; }
[ -n "$installation_id" ] || { usage; exit 2; }
[ -n "$migration_id" ] || { usage; exit 2; }
[ -n "${HERMES_MIGRATION_PSQL_COMMAND:-}" ] \
  || fail_harness 'HERMES_MIGRATION_PSQL_COMMAND is not set'
[ -r "$staging_file" ] \
  || fail_harness "staging file is unreadable: $staging_file"

case "$database" in
  *[!A-Za-z0-9_-]*)
    fail_harness 'database names may only carry [A-Za-z0-9_-]'
    ;;
esac

staging_document=$(cat "$staging_file") \
  || fail_harness "staging file could not be read: $staging_file"
[ -n "$staging_document" ] || fail_harness 'staging file is empty'

# The staging document and identifiers travel inside dollar-quoted SQL
# literals on the session's stdin; the quoting is sound only while the
# sentinel tag never appears in the payload bytes.
tag='hermes_v1_to_v2_runner'
for value in "$staging_document" "$installation_id" "$migration_id"; do
  case "$value" in
    *"$tag"*)
      fail_harness 'input contains the reserved runner quoting tag'
      ;;
  esac
done

# Substitute every literal {database} occurrence in the command template.
psql_command=''
remainder=$HERMES_MIGRATION_PSQL_COMMAND
substituted=0
while :; do
  case "$remainder" in
    *'{database}'*)
      psql_command="$psql_command${remainder%%\{database\}*}$database"
      remainder=${remainder#*\{database\}}
      substituted=1
      ;;
    *)
      psql_command="$psql_command$remainder"
      break
      ;;
  esac
done
[ "$substituted" -eq 1 ] \
  || fail_harness 'HERMES_MIGRATION_PSQL_COMMAND lacks the {database} placeholder'

transcript=$(mktemp) || fail_harness 'mktemp failed'
session=$(mktemp) || { rm -f "$transcript"; fail_harness 'mktemp failed'; }
trap 'rm -f "$transcript" "$session"' EXIT HUP INT TERM

# The controlled session script: ON_ERROR_STOP stays off so every governed
# rejection is branched on via :ERROR and recorded as append-only evidence
# before the session ends. The session advisory lock lives on this single
# connection for the entire run.
{
  printf '\\set ON_ERROR_STOP off\n'
  printf '\\pset format unaligned\n'
  printf '\\pset tuples_only on\n'
  printf 'SELECT $%s$%s$%s$ AS staging_document \\gset\n' \
    "$tag" "$staging_document" "$tag"
  printf 'SELECT $%s$%s$%s$ AS installation_id \\gset\n' \
    "$tag" "$installation_id" "$tag"
  printf 'SELECT $%s$%s$%s$ AS migration_id \\gset\n' \
    "$tag" "$migration_id" "$tag"
  cat <<'SESSION_EOF'
SELECT pg_try_advisory_lock(hashtextextended(
  'xfactory-v1-to-v2-migration:' || :'installation_id' || E'\n'
    || :'migration_id', 0)) AS lock_acquired \gset
\if :ERROR
  \echo hermes-v1-to-v2: outcome=lock-error
  \quit
\endif
\if :lock_acquired
\else
  \echo hermes-v1-to-v2: outcome=lock-unavailable
  \quit
\endif
BEGIN;
SELECT xfactory_runtime_api_v2.stage_migration(
  :'staging_document'::jsonb) AS staging_result \gset
\if :ERROR
  ROLLBACK;
  \echo hermes-v1-to-v2: outcome=staging-rejected
  \quit
\endif
SELECT xfactory_runtime_api_v2.begin_migration_attempt(
  :'installation_id', :'migration_id') AS begin_result \gset
\if :ERROR
  ROLLBACK;
  \echo hermes-v1-to-v2: outcome=begin-rejected
  \quit
\endif
COMMIT;
\if :ERROR
  \echo hermes-v1-to-v2: outcome=begin-commit-failed
  \quit
\endif
SELECT (:'begin_result'::jsonb ->> 'terminal') = 'true' AS already_terminal,
       (:'begin_result'::jsonb ->> 'attempt_id') AS attempt_id \gset
\if :already_terminal
  \echo hermes-v1-to-v2: result=:begin_result
  \echo hermes-v1-to-v2: outcome=converged-terminal-success
  \quit
\endif
BEGIN ISOLATION LEVEL SERIALIZABLE;
-- The twelve v1 table locks are taken as top-level utility statements, in
-- bytewise (schema, table) order, so every lock is held BEFORE the
-- serializable snapshot is established (a LOCK issued inside the cutover
-- function -- or wrapped in any SELECT -- would follow the snapshot and
-- could miss a v1 write committed during the lock wait). The cutover
-- function only verifies the locks are pre-held.
LOCK TABLE public.hermes_approval_requests IN SHARE ROW EXCLUSIVE MODE;
LOCK TABLE public.hermes_approvals IN SHARE ROW EXCLUSIVE MODE;
LOCK TABLE public.hermes_github_team_mappings IN SHARE ROW EXCLUSIVE MODE;
LOCK TABLE public.hermes_group_memberships IN SHARE ROW EXCLUSIVE MODE;
LOCK TABLE public.hermes_groups IN SHARE ROW EXCLUSIVE MODE;
LOCK TABLE public.hermes_job_artifacts IN SHARE ROW EXCLUSIVE MODE;
LOCK TABLE public.hermes_job_events IN SHARE ROW EXCLUSIVE MODE;
LOCK TABLE public.hermes_job_runs IN SHARE ROW EXCLUSIVE MODE;
LOCK TABLE public.hermes_jobs IN SHARE ROW EXCLUSIVE MODE;
LOCK TABLE public.hermes_profiles IN SHARE ROW EXCLUSIVE MODE;
LOCK TABLE public.hermes_traceability_edges IN SHARE ROW EXCLUSIVE MODE;
LOCK TABLE public.hermes_workers IN SHARE ROW EXCLUSIVE MODE;
\if :ERROR
  ROLLBACK;
  \echo hermes-v1-to-v2: cutover-error=:LAST_ERROR_MESSAGE
  SELECT xfactory_runtime_api_v2.fail_migration_attempt(
    :'installation_id', :'migration_id', :'attempt_id',
    'v1 table locks rejected: ' || :'LAST_ERROR_SQLSTATE');
  \if :ERROR
    \echo hermes-v1-to-v2: outcome=failure-append-rejected
    \quit
  \endif
  \echo hermes-v1-to-v2: outcome=attempt-failed
  \quit
\endif
SELECT xfactory_runtime_api_v2.execute_v1_cutover(
  :'installation_id', :'migration_id', :'attempt_id') AS cutover_result \gset
\if :ERROR
  ROLLBACK;
  \echo hermes-v1-to-v2: cutover-error=:LAST_ERROR_MESSAGE
  SELECT xfactory_runtime_api_v2.fail_migration_attempt(
    :'installation_id', :'migration_id', :'attempt_id',
    'cutover rejected: ' || :'LAST_ERROR_SQLSTATE');
  \if :ERROR
    \echo hermes-v1-to-v2: outcome=failure-append-rejected
    \quit
  \endif
  \echo hermes-v1-to-v2: outcome=attempt-failed
  \quit
\endif
COMMIT;
\if :ERROR
  \echo hermes-v1-to-v2: cutover-error=:LAST_ERROR_MESSAGE
  SELECT xfactory_runtime_api_v2.fail_migration_attempt(
    :'installation_id', :'migration_id', :'attempt_id',
    'cutover commit rejected: ' || :'LAST_ERROR_SQLSTATE');
  \if :ERROR
    \echo hermes-v1-to-v2: outcome=failure-append-rejected
    \quit
  \endif
  \echo hermes-v1-to-v2: outcome=attempt-failed
  \quit
\endif
\echo hermes-v1-to-v2: result=:cutover_result
\echo hermes-v1-to-v2: outcome=succeeded
SELECT pg_advisory_unlock(hashtextextended(
  'xfactory-v1-to-v2-migration:' || :'installation_id' || E'\n'
    || :'migration_id', 0));
SESSION_EOF
} > "$session"

# The template is deliberately expanded unquoted: it is a whitespace-split
# argv template per the runtime contract (no embedded quoting supported).
# shellcheck disable=SC2086
if $psql_command < "$session" > "$transcript" 2>&1; then
  psql_status=0
else
  psql_status=$?
fi

cat "$transcript"

if [ "$psql_status" -ne 0 ]; then
  printf 'hermes-v1-to-v2: harness-error: migration session ended abnormally (psql exit %s)\n' \
    "$psql_status" >&2
  exit 2
fi

outcome=$(sed -n 's/^hermes-v1-to-v2: outcome=//p' "$transcript" | tail -n 1)
case "$outcome" in
  succeeded|converged-terminal-success)
    exit 0
    ;;
  attempt-failed|staging-rejected|begin-rejected|begin-commit-failed|lock-unavailable)
    exit 1
    ;;
  *)
    printf 'hermes-v1-to-v2: harness-error: no terminal outcome marker\n' >&2
    exit 2
    ;;
esac
