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

#: Field names that carry credential MATERIAL. Refused anywhere in the hosting
#: record, in BOTH hosting cases — the self-hosted exemption is from declaring
#: custody, never from keeping secrets out of the repository.
#:
#: `session` and `profile` are here for a reason worth stating: the `nlm`
#: profile is refreshable SESSION STATE, which `credential-contracts` refuses to
#: distribute as a class because an ephemeral copy's refresh silently stales the
#: master. Pasting one into this record would be that defect with the copy left
#: implicit.
SECRET_SHAPED_FIELDS = frozenset({
    "password", "passphrase", "secret", "token", "api_key", "apikey",
    "totp", "totp_seed", "otp_seed", "recovery_code", "recovery_codes",
    "backup_code", "backup_codes", "cookie", "cookies", "session",
    "session_token", "profile", "exported_profile", "private_key",
    "credential", "credentials",
})


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

    _check_custody(hosting, case, errors)


def _check_custody(hosting, case, errors: list[str]) -> None:
    """The credential's custody: declared BY REFERENCE, or not at all.

    add-notebook-hosting-credential-custody § 2. Two obligations, and the second
    is the one that does the work:

      * an OPERATOR-HOSTED declaration names the binding that holds its
        account's credential — an operated identity with no declared custody is
        not governed, it is merely undocumented;
      * NOTHING SECRET-SHAPED appears in this record at all, in either case.

    The self-hosted case is deliberately exempt from the FIRST and never from
    the SECOND. An individual operating their own account has no operator to
    bear the custody obligation (the two-case model this capability already
    holds elsewhere) — but a password written into a self-hosted record is just
    as leaked as one written into an operator-hosted record.
    """
    custody = hosting.get("custody")

    # The secret-shaped refusal runs FIRST and over the whole hosting block, not
    # just the custody sub-tree, because the failure being prevented is material
    # in the file — and material does not care which key it was filed under.
    _refuse_secret_shaped(hosting, "hosting", errors)

    if custody is None:
        if case == "operator_hosted":
            _err(errors,
                 "hosting.custody: an operator-hosted declaration MUST name "
                 "where the account's credential is held. Without it the "
                 "identity is undocumented rather than governed, and nobody but "
                 "whoever created the account can operate it — which is the "
                 "condition moving off a personal identity exists to remove. "
                 "The remedy is a binding reference (binding_kind / "
                 "binding_client / binding_id), never the secret")
        return

    if not isinstance(custody, dict):
        _err(errors, "hosting.custody: must be a mapping carrying a binding "
                     "reference")
        return

    for field in ("binding_kind", "binding_client", "binding_id"):
        if not custody.get(field):
            _err(errors, f"hosting.custody.{field}: the custody reference must "
                         f"IDENTIFY THE BINDING. All three of binding_kind, "
                         f"binding_client and binding_id are required — a "
                         f"partial reference cannot be resolved through the "
                         f"governed path, which is the only way this record is "
                         f"meant to be usable")

    covers = custody.get("covers")
    if not isinstance(covers, list) or not covers:
        _err(errors, "hosting.custody.covers: name every secret the binding "
                     "holds. Custody must cover what the identity actually "
                     "needs to authenticate, not the primary factor alone — a "
                     "password in a vault beside a TOTP seed on someone's phone "
                     "is a single point of failure wearing governance")

    # CUSTODY IS NOT AUTOMATION, and the record must not imply it is. A
    # reference that suggests unattended access the install does not have is
    # worse than none, because it invites a reader to plan on it.
    if custody.get("interactive_step_remains") is True:
        if not str(custody.get("interactive_step") or "").strip():
            _err(errors,
                 "hosting.custody.interactive_step: the record declares an "
                 "interactive step remains but does not say what it is. Name "
                 "it — a reader deciding whether the projection can run "
                 "unattended needs the answer here, not in a runbook they may "
                 "not open")
    elif "interactive_step_remains" not in custody:
        _err(errors,
             "hosting.custody.interactive_step_remains: state plainly whether "
             "the custody material alone completes the platform's sign-in. "
             "Silence reads as 'yes' to an operator planning automation, and "
             "for this platform the honest answer is no")


def _refuse_secret_shaped(node, path: str, errors: list[str]) -> None:
    """Refuse credential MATERIAL anywhere under the hosting record.

    Keyed on the field NAME rather than on the value's shape. A value-shaped
    heuristic ("does this look like a password?") is exactly the wrong control
    here: it fails open on anything unusual, and the one thing worse than no
    check is a check that says a leaked secret looks fine.

    `secret_ref` is refused too, and it is not secret material. It is BINDING
    DETAIL — the record's job is to point AT the binding, and carrying its
    fields here invites the rest of the binding to follow (review note,
    2026-08-23). The refusal names the binding as the remedy rather than
    redaction in place, because a redacted secret is still a secret that was
    committed.
    """
    # SEQUENCES ARE WALKED TOO. An earlier version descended only into mappings,
    # so `hosting.anything: [{password: hunter2}]` was skipped outright and the
    # record validated clean with credential material sitting in it (Copilot,
    # PR #395; reproduced before this fix, and again after, as a mutation).
    #
    # That was the fail-open family INSIDE the refusal written to prevent it: a
    # path that could not answer returned "nothing to see" instead of looking.
    # YAML nests freely, and a walk that covers one container type is not a walk
    # — the recursion is over the DOCUMENT, not over the shape a reader expects.
    if isinstance(node, (list, tuple)):
        for index, item in enumerate(node):
            _refuse_secret_shaped(item, f"{path}[{index}]", errors)
        return
    if not isinstance(node, dict):
        return
    for key, value in node.items():
        lowered = str(key).lower()
        if lowered in SECRET_SHAPED_FIELDS:
            _err(errors,
                 f"{path}.{key}: credential material MUST NOT appear in the "
                 f"hosting record, in this repository, or in any projection "
                 f"artifact. THE REMEDY IS A BINDING REFERENCE, NOT REDACTION "
                 f"IN PLACE — a redacted secret is a secret that was already "
                 f"committed, and the fix is to rotate it and point at the "
                 f"binding that holds the new one")
        elif lowered == "secret_ref":
            _err(errors,
                 f"{path}.secret_ref: this is BINDING DETAIL and does not "
                 f"belong in the hosting record. Name the binding "
                 f"(binding_kind / binding_client / binding_id); the binding "
                 f"instance carries the provider, vault, secret_ref, owner and "
                 f"rotation policy, and it lives in the consuming install")
        _refuse_secret_shaped(value, f"{path}.{key}", errors)


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
