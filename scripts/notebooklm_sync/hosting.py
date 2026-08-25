from __future__ import annotations

import json
from collections.abc import Callable
from pathlib import Path

from .models import HOSTING_MIGRATION_SCALARS, HOSTING_REL, HOSTING_SCALARS
from .nlm_client import JsonValue

NON_USER_MARKERS = (".iam.gserviceaccount.com", ".gserviceaccount.com")
MIGRATION_STATES = (None, "", "pending", "complete")


def profile_account(profile: str, home: Path | None = None) -> str | None:
    base = home or (Path.home() / ".notebooklm-mcp-cli")
    path = base / "profiles" / profile / "metadata.json"
    try:
        parsed: JsonValue = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    if not isinstance(parsed, dict):
        return None
    email = parsed.get("email")
    return email.strip() or None if isinstance(email, str) else None


def read_hosting_declaration(root: Path) -> dict[str, str] | None:
    path = root / HOSTING_REL
    if not path.is_file():
        return None
    found: dict[str, str] = {}
    in_hosting = False
    in_migration = False
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.split("#", 1)[0].rstrip()
        if not line.strip():
            continue
        indent = len(line) - len(line.lstrip())
        if indent == 0:
            in_hosting = line.strip() == "hosting:"
            in_migration = False
            continue
        if not in_hosting:
            continue
        key, separator, raw_value = line.strip().partition(":")
        value = raw_value.strip().strip('"').strip("'")
        if indent == 2:
            in_migration = key == "migration" and not value
            if separator and key in HOSTING_SCALARS:
                found[key] = value
        elif (
            indent == 4
            and in_migration
            and key in HOSTING_MIGRATION_SCALARS
        ):
            found[f"migration_{key}"] = value
    return found


def refuse_unusable_declaration(declared: dict[str, str]) -> None:
    if not declared:
        raise SystemExit(
            f"hosting: {HOSTING_REL} EXISTS but no declaration could be read "
            "from it. The sync reads the `hosting:` block's own two-space "
            "scalars; flow style, other indentation or tabs parse as valid "
            "YAML for the validator and as nothing here. Refusing rather than "
            "running unbound — an unreadable declaration is not an absent "
            "one. Re-indent it to match "
            "examples/notebook-projection-hosting.yaml."
        )
    case = declared.get("case")
    account = declared.get("account", "")
    state = declared.get("migration_state")
    if state not in MIGRATION_STATES:
        raise SystemExit(
            f"hosting: migration.state is {state!r}; it is 'pending', "
            "'complete', or absent. An unrecognized state would otherwise "
            "bind the run to the DECLARED profile while the books are still "
            "in the previous account — a premature migration under --apply."
        )
    if state == "pending" and not declared.get("migration_from_nlm_profile"):
        raise SystemExit(
            "hosting: a PENDING migration must name "
            "migration.from_nlm_profile — the sync binds there until the "
            "books move, and cannot bind to a profile nobody named."
        )
    if not declared.get("nlm_profile"):
        raise SystemExit(
            f"hosting: {HOSTING_REL} names no top-level nlm_profile. It is "
            "required in every state: it is what the run binds to once a "
            "migration completes."
        )
    if case not in ("operator_hosted", "self_hosted"):
        raise SystemExit(
            f"hosting: {HOSTING_REL} declares case {case!r}; an install "
            "declares exactly one of operator_hosted or self_hosted"
        )
    if "@" not in account:
        raise SystemExit(f"hosting: {HOSTING_REL} names no usable account address")
    if any(marker in account for marker in NON_USER_MARKERS):
        raise SystemExit(
            f"hosting: {account} is a service account. The hosting identity "
            "MUST be a Google USER account — NotebookLM has no API and a "
            "service account cannot drive its consumer web UI, so this "
            "declaration could never work"
        )
    if case != "operator_hosted":
        return
    if declared.get("account_type") != "google_workspace_user":
        raise SystemExit(
            f"hosting: {account} is declared operator-hosted but its "
            f"account_type is {declared.get('account_type')!r}. The "
            "operator-hosted case requires a google_workspace_user: a "
            "consumer account keeps a personal recovery path and no admin "
            "console, which is what this case exists to remove"
        )
    domain = declared.get("domain", "")
    if not domain:
        raise SystemExit(
            "hosting: an operator-hosted declaration must name the domain "
            "the operating party administers"
        )
    if not account.lower().endswith("@" + domain.lower()):
        raise SystemExit(
            f"hosting: {account} is not in the declared domain {domain} — "
            "the operating party must administer the account it declares"
        )


def enforce_hosting_profile(
    root: Path,
    *,
    active_profile: Callable[[], str | None],
    account_for: Callable[[str], str | None],
    bind: Callable[[str | None], None],
) -> dict[str, str] | None:
    declared = read_hosting_declaration(root)
    if declared is None:
        bind(None)
        print(
            "hosting: NO DECLARED HOSTING IDENTITY. This install does not "
            "meet the declared-hosting requirement — a transition state, not "
            "a third legitimate case. Running under the CLI's default "
            "profile; this projection is not governed by a declared account."
        )
        return None

    refuse_unusable_declaration(declared)
    account = declared.get("account") or "<unnamed>"
    case = declared.get("case") or "<unstated>"
    target = declared.get("nlm_profile")
    pending = declared.get("migration_state") == "pending"
    profile = declared.get("migration_from_nlm_profile") if pending else target
    holder = (
        declared.get("migration_from_account", "the previous account")
        if pending
        else account
    )
    if profile is None:
        raise SystemExit("hosting: declaration resolved no usable profile")

    active = active_profile()
    if active is None:
        raise SystemExit(
            "hosting: cannot read the CLI's active profile, so this run "
            "cannot prove which account it would write to. Refusing rather "
            "than guessing."
        )
    if active != profile:
        raise SystemExit(
            f"hosting: expected the {profile!r} profile but the CLI's active "
            f"profile is {active!r}. Refusing: a run that cannot prove which "
            "account it writes to is the failure this declaration exists to "
            "retire.\n"
            f"  switch it with:   nlm login switch {profile}\n"
            f"  first time:       nlm login --profile {profile}"
        )

    expected = holder if pending else account
    signed_in = account_for(profile)
    if signed_in and expected and signed_in.lower() != expected.lower():
        raise SystemExit(
            f"hosting: profile {profile!r} is signed in as {signed_in}, but "
            f"this install expects {expected}. Refusing: the profile name "
            "matches and the ACCOUNT does not, which is exactly the mix-up a "
            "declared identity exists to catch.\n"
            f"  re-authenticate with:  nlm login --profile {profile}  "
            f"(as {expected})"
        )
    if signed_in is None:
        print(
            f"hosting: profile {profile!r} records no account address "
            "(an older login leaves it null) — the binding is verified by "
            "profile NAME only; confirm with `nlm notebook list` that it "
            f"shows {expected}."
        )

    bind(profile)
    if pending:
        print(
            f"hosting: MIGRATION PENDING. Declared {case} {account}, but the "
            f"books still live in {holder} under profile {profile!r} "
            "(verified active). This run reconciles them THERE. See "
            "docs/notebook-projection-migration-runbook.md."
        )
    else:
        print(
            f"hosting: {case} — {account} "
            f"(nlm profile {profile!r}, verified active)"
        )
    return declared
