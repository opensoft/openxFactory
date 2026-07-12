# SOP: OpenAI Realtime F0 Lab Credential

- Status: active
- Owner: openxFactory avatar platform maintainers
- Applies to: `experiments/avatar-brokered-call` and feature `002-avc-f0-feasibility`

## Purpose

This SOP defines how to provision and use the OpenAI credential for the avatar
brokered-call F0 lab without exposing the credential in Git, command arguments, logs,
evidence, Hermes memory, or a persistent worker environment. It implements the
[xFactory Credential Access Model](../credential-access-model.md).

## Credential Record

| Field | Non-secret value |
| --- | --- |
| Requirement ID | `openai_realtime_f0_lab` |
| Logical secret reference | `openxfactory/lab/openai/realtime-f0` |
| Runtime contract | `OPENAI_API_KEY` process environment variable |
| Candidate pinned by the F0 contract | `gpt-realtime-2.1` |
| Credential registry account | `openxfactory-realtime-f0-lab` |
| Encrypted recovery reference | `escrow/openai/openxfactory-realtime-f0-lab.credentials.json.age` in `xFactory-Agents-Credential-Registry` |
| Local development binding | `$HOME/.ai-keys/openai.key` |
| Hosted or CI binding | Approved secret manager; inject as a protected environment secret |
| Allowed use | Dedicated lab project, generated audio, tools disabled, no tenant data |

The logical reference and this SOP belong in openxFactory. Account metadata and an
approved `age`-encrypted recovery copy belong in the private
`xFactory-Agents-Credential-Registry`. The plaintext API key does not belong in either Git
repository. A project API key is not model-specific: provider entitlement determines
which models that project can use. A valid key therefore does not prove that the pinned
candidate is available; authentication and candidate access are separate checks.

## Provisioning Requirements

1. Create the key in a dedicated OpenAI lab project, not a personal or production
   project shared with unrelated workloads.
2. Assign an owner and configure project budget and rate controls before live trials.
3. Use the minimum provider permissions that support model discovery and the Realtime
   experiment. Do not enable tenant tools or attach production data.
4. Transfer the value through an approved password or secret manager, or directly into
   the hidden local prompt below. Do not paste it into chat, an issue, a commit, a shell
   command, or a CLI argument.

## Install or Rotate the Local Binding

Run this from an interactive WSL shell. Input is hidden and does not enter shell history.
The write is atomic, the directory is mode `700`, and the file is mode `600`.

```bash
(
  set -eu
  secret_dir="$HOME/.ai-keys"
  secret_file="$secret_dir/openai.key"
  install -d -m 700 "$secret_dir"
  umask 077
  printf 'Paste the OpenAI lab API key: ' >&2
  IFS= read -r -s key </dev/tty
  printf '\n' >&2
  case "$key" in
    sk-*) ;;
    *) printf 'Input does not look like an OpenAI API key. Nothing written.\n' >&2; exit 1 ;;
  esac
  case "$key" in
    *[!A-Za-z0-9_-]*) printf 'Key contains unexpected characters. Nothing written.\n' >&2; exit 1 ;;
  esac
  tmp="$(mktemp "$secret_dir/.openai.key.XXXXXX")"
  trap 'rm -f "$tmp"' EXIT
  printf '%s\n' "$key" >"$tmp"
  chmod 600 "$tmp"
  mv "$tmp" "$secret_file"
  trap - EXIT
  printf 'Installed %s with mode %s\n' "$secret_file" "$(stat -c '%a' "$secret_file")"
)
```

Do not place this file under a repository, add it to a shell startup file, or copy it into
`py-bench`. Repo-level `.env` patterns are ignored as defense in depth, not as an approved
secret store. Existing workBench launchers read this host path and export
`OPENAI_API_KEY` for a launched process.

## Encrypted Registry Recovery Copy

The private `xFactory-Agents-Credential-Registry` stores the account record, provider
policy, ciphertext digest, and `age` ciphertext. Follow that repository's recipient and
round-trip validation policy whenever the key rotates. The escrow copy is supervised
recovery material only: it is not a deployment source and must not be copied into this
repository or automatically restored into a host or container.

## Load for One Host Session

```bash
secret_file="$HOME/.ai-keys/openai.key"
test "$(stat -c '%a' "$secret_file")" = 600
OPENAI_API_KEY="$(tr -d '\r\n' <"$secret_file")"
export OPENAI_API_KEY
test -n "${OPENAI_API_KEY:-}" && printf 'OPENAI_API_KEY=present\n'
```

Never run `printenv OPENAI_API_KEY`, dump the full environment, or enable shell tracing
while the key is loaded. Remove it from the shell when finished:

```bash
unset OPENAI_API_KEY
```

## Verify Authentication Without Disclosure

After loading the variable, this check prints only the HTTP result and whether the pinned
candidate appears in the model list. It does not print the key or provider response body.

```bash
python3 - <<'PY'
import json
import os
import urllib.error
import urllib.request

key = os.environ.get("OPENAI_API_KEY")
if not key:
    raise SystemExit("OPENAI_API_KEY is absent")

request = urllib.request.Request(
    "https://api.openai.com/v1/models",
    headers={"Authorization": f"Bearer {key}"},
)
try:
    with urllib.request.urlopen(request, timeout=30) as response:
        payload = json.load(response)
except urllib.error.HTTPError as error:
    raise SystemExit(f"credential check failed: HTTP {error.code}") from None

models = {item.get("id") for item in payload.get("data", [])}
print("credential=valid")
print("gpt-realtime-2.1=" + ("listed" if "gpt-realtime-2.1" in models else "not-listed"))
PY
```

`not-listed` is not permission to substitute a model silently. Record the result and
resolve the candidate contract before live execution.

## Inject Into `py-bench` for One Command

Load the host variable as above, then pass its name into one `docker exec`. Do not persist
it in the container configuration or write it to the mounted workspace.

```bash
docker exec --env OPENAI_API_KEY py-bench sh -lc '
  test -n "$OPENAI_API_KEY" && printf "OPENAI_API_KEY=present\n"
'
unset OPENAI_API_KEY
```

Use the same injection pattern around the supervised F0 command only after the live
transport gate below is cleared.

## Live Transport Gate

Credential readiness is not live-runtime readiness. At the time of this SOP, the live
broker, sideband, media, and test paths are explicit stubs, and `avatar-f0 run` emits an
`INCONCLUSIVE` record with reason `live_path_deferred` even when the key is present.

Before claiming or starting the 70-trial provider matrix:

1. Implement and review the live broker, sideband, and media clients.
2. Replace the supervised live-test skip with executable provider assertions.
3. Prove redaction and bounded cleanup against failure injection.
4. Authenticate the key and confirm the exact candidate is available to the lab project.
5. Obtain the required human approval for a cost-incurring live run.

## Rotation and Revocation

1. Create a replacement key in the same dedicated lab project.
2. Install it atomically using the local procedure or update the approved secret-manager
   version.
3. Run the non-disclosing authentication check.
4. Revoke the old key at the provider.
5. Record owner, rotation date, reason, and logical secret reference. Never record the
   key value.

If a key appears in Git, chat, logs, evidence, screenshots, or command history, treat it
as compromised: revoke it immediately, issue a replacement, remove the exposed artifact,
scan the repository and relevant logs, and record the incident. Deleting the value in a
later commit does not make the exposed key safe.
