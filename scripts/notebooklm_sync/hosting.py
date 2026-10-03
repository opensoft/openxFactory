from __future__ import annotations

import json
from collections.abc import Callable
from pathlib import Path

from . import hosting_validation
from .hosting_paths import HOSTING_CONFIG_REL, HOSTING_ENV, hosting_declaration_path
from .models import HOSTING_MIGRATION_SCALARS, HOSTING_SCALARS
from .nlm_client import JsonValue, configured_nlm_profile, decode_json

refuse_unusable_declaration = hosting_validation.refuse_unusable_declaration

NON_USER_MARKERS = (".iam.gserviceaccount.com", ".gserviceaccount.com")
MIGRATION_STATES = (None, "", "pending", "complete")


def profile_account(profile: str, home: Path | None = None) -> str | None:
    base = home or (Path.home() / ".notebooklm-mcp-cli")
    path = base / "profiles" / profile / "metadata.json"
    try:
        parsed = decode_json(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    if not isinstance(parsed, dict):
        return None
    email = parsed.get("email")
    return email.strip() or None if isinstance(email, str) else None


def read_hosting_declaration(root: Path) -> dict[str, str] | None:
    path = hosting_declaration_path(root)
    if path is None or not path.is_file():
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
            if separator and key in (*HOSTING_SCALARS, "instance"):
                found[key] = value
        elif indent == 4 and in_migration and key in HOSTING_MIGRATION_SCALARS:
            found[f"migration_{key}"] = value
    return found


def enforce_hosting_profile(
    root: Path,
    *,
    active_profile: Callable[[], str | None],
    account_for: Callable[[str], str | None],
    bind: Callable[[str | None], None],
) -> dict[str, str] | None:
    resolved = hosting_declaration_path(root)
    declared = read_hosting_declaration(root)
    if declared is None:
        bind(None)
        print(
            "hosting: NO DECLARED HOSTING IDENTITY. This install does not "
            + "meet the declared-hosting requirement — a transition state, not "
            + "a third legitimate case. Running under the CLI's default "
            + "profile; this projection is not governed by a declared account."
        )
        if resolved is not None:
            print(
                f"hosting: configuration names {resolved}, which is not a readable file. That is why this run is undeclared: the path is configured and the record is not there."
            )
        else:
            print(
                f"hosting: nothing is configured. Set {HOSTING_CONFIG_REL}'s `declaration_path:` or {HOSTING_ENV} to this install's own declaration; the committed example is a fixture and is deliberately not a fallback."
            )
        return None

    refuse_unusable_declaration(declared, str(resolved) if resolved else None)
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
            + "cannot prove which account it would write to. Refusing rather "
            + "than guessing."
        )
    if active != profile:
        raise SystemExit(
            f"hosting: expected the {profile!r} profile but the CLI's active "
            + f"profile is {active!r}. Refusing: a run that cannot prove which "
            + "account it writes to is the failure this declaration exists to "
            + "retire.\n"
            + f"  switch it with:   nlm login switch {profile}\n"
            + f"  first time:       nlm login --profile {profile}"
        )

    expected = holder if pending else account
    signed_in = account_for(profile)
    if signed_in and expected and signed_in.lower() != expected.lower():
        raise SystemExit(
            f"hosting: profile {profile!r} is signed in as {signed_in}, but "
            + f"this install expects {expected}. Refusing: the profile name "
            + "matches and the ACCOUNT does not, which is exactly the mix-up a "
            + "declared identity exists to catch.\n"
            + f"  re-authenticate with:  nlm login --profile {profile}  "
            + f"(as {expected})"
        )
    if signed_in is None:
        print(
            f"hosting: profile {profile!r} records no account address "
            + "(an older login leaves it null) — the binding is verified by "
            + "profile NAME only; confirm with `nlm notebook list` that it "
            + f"shows {expected}."
        )

    bind(profile)
    if pending:
        print(
            f"hosting: MIGRATION PENDING. Declared {case} {account}, but the "
            + f"books still live in {holder} under profile {profile!r} "
            + "(verified active). This run reconciles them THERE. See "
            + "docs/notebook-projection-migration-runbook.md."
        )
    else:
        print(f"hosting: {case} — {account} (nlm profile {profile!r}, verified active)")
    return declared


def active_nlm_profile(runner: Callable[..., JsonValue] | None = None) -> str | None:
    if runner is None:
        return configured_nlm_profile()
    try:
        output = runner("config", "get", "auth.default_profile", parse=False)
    except (OSError, RuntimeError, TypeError, ValueError):
        return None
    return output.strip() or None if isinstance(output, str) else None
