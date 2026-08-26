#!/usr/bin/env python3
"""Validate the notebook projection's hosting declaration and share-out roster.

Governs `examples/notebook-projection-hosting.yaml`, the record ratified by
`add-notebook-projection-identity` (2026-08-23).

WHY THIS IS NOT A `contracts/` SCHEMA. The record is the operator's own
governance artifact for one install's tooling account: no other repository,
install or domain consumes it and nothing pins it, which is what
`contracts/` membership is for. Its sibling `lifecycle-notebook-workspaces.yaml`
— the workspace registry for this same projection, read and written by the same
sync — lives beside it for the same reason. Promoting the shape into
`contracts/` is a later, deliberate act if a second install ever needs to
interoperate on it; that act, not this one, would carry the release ritual.

What is checked, all of it from the ratified requirements:

  * the two-case vocabulary — `operator_hosted` or `self_hosted`, nothing else;
  * an operator-hosted declaration names a Workspace USER account in a domain
    it administers, and the account's domain matches the declared domain;
  * no provider service account may be named — NotebookLM has no API and a
    service account cannot drive its consumer web UI, so such a declaration
    could never work;
  * the run-binding field the sync needs (`nlm_profile`) is present;
  * a PENDING migration names both the account the books still live in and its
    profile, because the sync binds to that until the books move;
  * every roster entry carries the six ratified fields;
  * roster UNIQUENESS is `(hosting_account, user, book_or_alias)` — role,
    grant time and granting actor are attributes, so a re-decision updates the
    one live entry instead of asserting a stale grant beside a current one.

Exit 0 when the record conforms, 1 otherwise.
"""

from __future__ import annotations

import sys
from pathlib import Path

import yaml

DEFAULT_REL = "examples/notebook-projection-hosting.yaml"
CASES = ("operator_hosted", "self_hosted")
ENTRY_FIELDS = ("hosting_account", "user", "book_or_alias", "role",
                "granted_at", "granted_by")
KEY_FIELDS = ("hosting_account", "user", "book_or_alias")
ROLES = ("viewer", "editor")
# The shapes a Google *user* account never has. A projection host must be one:
# there is no API, and a service principal cannot drive the consumer web UI.
NON_USER_MARKERS = (".iam.gserviceaccount.com", ".gserviceaccount.com")


def _err(errors: list[str], msg: str) -> None:
    errors.append(msg)


def _check_hosting(hosting, errors: list[str]) -> None:
    if not isinstance(hosting, dict):
        _err(errors, "hosting: must be a mapping naming the declared identity")
        return

    case = hosting.get("case")
    if case not in CASES:
        _err(errors, f"hosting.case: {case!r} is not one of {', '.join(CASES)} "
                     f"— an install declares exactly one of the two cases")

    account = hosting.get("account")
    if not isinstance(account, str) or "@" not in account:
        _err(errors, "hosting.account: a Google user account address is required")
        account = ""

    if any(marker in account for marker in NON_USER_MARKERS):
        _err(errors, f"hosting.account: {account} is a service account. The "
                     f"hosting identity MUST be a Google USER account — "
                     f"NotebookLM has no API and a service account cannot "
                     f"drive its consumer web UI")

    if case == "operator_hosted":
        if hosting.get("account_type") != "google_workspace_user":
            _err(errors, "hosting.account_type: an operator-hosted declaration "
                         "must name a google_workspace_user — a consumer "
                         "account keeps a personal recovery path and no admin "
                         "console, which is what this case exists to remove")
        domain = hosting.get("domain")
        if not isinstance(domain, str) or not domain:
            _err(errors, "hosting.domain: an operator-hosted declaration names "
                         "the domain the operating party administers")
        elif account and not account.lower().endswith("@" + domain.lower()):
            _err(errors, f"hosting.account: {account} is not in the declared "
                         f"domain {domain} — the operating party must "
                         f"administer the account it declares")

    if not hosting.get("nlm_profile"):
        _err(errors, "hosting.nlm_profile: the sync binds a run to an account "
                     "through its CLI profile and cannot bind to an unnamed one")

    migration = hosting.get("migration")
    if migration is not None:
        if not isinstance(migration, dict):
            _err(errors, "hosting.migration: must be a mapping when present")
        elif migration.get("state") == "pending":
            for field in ("from_account", "from_nlm_profile"):
                if not migration.get(field):
                    _err(errors, f"hosting.migration.{field}: a PENDING "
                                 f"migration must name where the books still "
                                 f"live — the sync binds there until they move")
        elif migration.get("state") not in (None, "complete"):
            _err(errors, f"hosting.migration.state: {migration.get('state')!r} "
                         f"is neither 'pending' nor 'complete'")


def _check_roster(record, hosting_account, errors: list[str]) -> None:
    entries = record.get("share_out")
    if entries is None:
        entries = []
    if not isinstance(entries, list):
        _err(errors, "share_out: must be a list of roster entries")
        return

    seen: dict[tuple, int] = {}
    for index, entry in enumerate(entries):
        where = f"share_out[{index}]"
        if not isinstance(entry, dict):
            _err(errors, f"{where}: must be a mapping")
            continue
        for field in ENTRY_FIELDS:
            if not entry.get(field):
                _err(errors, f"{where}.{field}: required — every governed share "
                             f"act records all six fields")
        if entry.get("role") not in ROLES and entry.get("role"):
            _err(errors, f"{where}.role: {entry.get('role')!r} is not one of "
                         f"{', '.join(ROLES)}")
        if hosting_account and entry.get("hosting_account") not in (None, hosting_account):
            _err(errors, f"{where}.hosting_account: {entry.get('hosting_account')} "
                         f"is not this install's declared hosting account "
                         f"{hosting_account}")
        key = tuple(entry.get(f) for f in KEY_FIELDS)
        if all(part for part in key):
            if key in seen:
                _err(errors, f"{where}: duplicate share-out key "
                             f"{key} — already recorded at "
                             f"share_out[{seen[key]}]. A re-approval, a role "
                             f"change or a grant by another actor UPDATES the "
                             f"live entry; two entries would let the roster "
                             f"assert a stale grant beside the current one")
            else:
                seen[key] = index

    denied = record.get("denied")
    if denied is not None and not isinstance(denied, list):
        _err(errors, "denied: must be a list when present")


def validate(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        record = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        return [f"{path}: unreadable ({exc})"]
    if not isinstance(record, dict):
        return [f"{path}: must be a mapping"]

    if record.get("schema_version") != 1:
        _err(errors, "schema_version: must be 1")
    if record.get("kind") != "notebook_projection_hosting":
        _err(errors, "kind: must be notebook_projection_hosting")

    hosting = record.get("hosting")
    _check_hosting(hosting, errors)
    account = hosting.get("account") if isinstance(hosting, dict) else None
    _check_roster(record, account, errors)
    return errors


def main(argv: list[str]) -> int:
    repo_root = Path(__file__).resolve().parent.parent
    path = Path(argv[1]) if len(argv) > 1 else repo_root / DEFAULT_REL
    if not path.is_file():
        print(f"validate-notebook-projection-hosting: {path} not found "
              f"— this install has NOT declared a hosting identity, which is a "
              f"transition state rather than a passing one")
        return 1
    errors = validate(path)
    for error in errors:
        print(f"{path.name}: {error}")
    print(f"validate-notebook-projection-hosting: {len(errors)} error(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
