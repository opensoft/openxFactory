#!/usr/bin/env python3
"""Validate the notebook projection's hosting declaration and share-out roster.

Governs the hosting record ratified by `add-notebook-projection-identity`
(2026-08-23), of which there are now TWO instances
(`adopt-configured-notebook-hosting-identity`, 2026-09-08): the SYNTHETIC one
committed here at `examples/notebook-projection-hosting.yaml`, which is the
shape's example and this script's default fixture, and an install's own LIVE
declaration, which lives wherever configuration says and is validated by
`--resolved`. The split exists because the record's addresses are the values an
implementation compares against a live Google account — so they could not be
redacted in place — and this repository is becoming public.

WHAT `--resolved` IS FOR. It is the operator check that replaces the CI one.
While the live record and the committed file were the same file,
`test_the_committed_record_conforms` was the live declaration's only automatic
conformance check; after the split, this repository's CI cannot reach the live
record without publishing it. `--resolved` is the command whose green line is
that record's conformance evidence, which is why it REFUSES to fall back to the
fixture and refuses a record marked as one.

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

import os
import sys
from pathlib import Path

import yaml

#: THE SHIPPED SYNTHETIC FIXTURE — not this install's declaration.
#: `adopt-configured-notebook-hosting-identity` (ratified 2026-09-08) split one
#: file into two: the live record lives in a configured, private home because
#: its `account`, its `migration.from_account` and its roster rows are the
#: values an implementation compares against a live Google account, and this
#: repository is becoming public. This path stays what it was (OQ-C: renaming it
#: would move twenty-one references for a signal a FIELD carries better) and the
#: record itself now says which kind of instance it is.
DEFAULT_REL = "examples/notebook-projection-hosting.yaml"
#: The resolution order, shared with `scripts/sync-notebooklm-books.py`.
#: TWO IMPLEMENTATIONS OF ONE ORDER, and that is deliberate: the sync carries no
#: YAML dependency and must not gain one, and it is HANDED its workspace root
#: (so it may not look outside it), while this validator takes no root argument
#: and discovers one. `tests/notebooklm/test_validate_hosting.py::
#: TheResolutionOrderIsOneOrder` refuses them to diverge on the order itself.
HOSTING_ENV = "XFACTORY_NOTEBOOK_HOSTING_DECLARATION"
HOSTING_CONFIG_REL = ".xfactory/notebook-hosting.yaml"
#: The `hosting.instance` value that marks a record as a fixture.
HOSTING_EXAMPLE_MARKER = "example"
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
    actor = _check_approval(record, hosting, errors)
    _check_roster(record, account, errors)
    _check_grants_are_by_the_designated_actor(record, actor, errors)
    return errors


def _check_approval(record, hosting, errors: list[str]):
    """The approval lane's designation, enforced (task 2.4).

    Returns the declared actor, or None when there is none to cross-check with.

    ADDED after review found the block was decoration: `validate()` read the
    hosting map and the roster and nothing else, so the whole `approval:` block
    could be DELETED, replaced with a scalar, or have `automated_approval`
    flipped to true, and the record still passed. A declaration nothing checks is
    the CPL-1b shape this change family keeps refusing — a control asserted
    somewhere no rule holds it.

    SCOPED LIKE CUSTODY, and for the same reason: an OPERATOR-HOSTED record must
    designate an actor, because a share request arriving at an operated account
    with nobody named is exactly what the ratified requirement forbids ("SHALL
    NOT be left to whoever happens to read the account's mail"). A SELF-HOSTED
    record need not: an individual deciding access to their own books is not a
    governance gap.
    """
    approval = record.get("approval")
    case = hosting.get("case") if isinstance(hosting, dict) else None

    if approval is None:
        if case == "operator_hosted":
            _err(errors,
                 "approval: an operator-hosted record MUST designate the "
                 "company-policy actor who decides share requests. Without it a "
                 "request is left to whoever happens to read the account's mail, "
                 "which is the failure this lane exists to prevent. Declare "
                 "approval.designated_actor")
        return None

    if not isinstance(approval, dict):
        _err(errors, "approval: must be a mapping carrying designated_actor — a "
                     "bare name cannot also carry where the act happens or "
                     "whether automation is permitted")
        return None

    actor = approval.get("designated_actor")
    if not isinstance(actor, str) or not actor.strip():
        _err(errors, "approval.designated_actor: name the person who decides. An "
                     "empty designation is the same as none")
        actor = None

    # THE RATIFIED POSTURE, not a default. "The approval SHALL remain a governed
    # human act either way" — so this field may be stated and may be false, and
    # may never be true. Detection and relay may be automated; the DECISION may
    # not.
    if approval.get("automated_approval") is not False:
        _err(errors,
             "approval.automated_approval: must be present and FALSE. The "
             "ratified requirement keeps the approval a governed human act even "
             "if the platform ever exposes a surface for detection and relay; a "
             "record claiming otherwise asserts a posture no requirement permits")

    if not str(approval.get("acts_in") or "").strip():
        _err(errors, "approval.acts_in: say where the act happens. The platform "
                     "exposes no approval API, so the interface is part of the "
                     "procedure rather than an implementation detail")

    return actor.strip() if isinstance(actor, str) and actor.strip() else None


def _check_grants_are_by_the_designated_actor(record, actor, errors: list[str]):
    """A grant recorded by anyone other than the designated actor is refused.

    THE CROSS-CHECK WITH TEETH. Designating an actor and then recording grants
    under another name would leave the designation decorative in the one place it
    is supposed to bind. The roster entry's `granted_by` is the record of WHO
    DID; the standing block is who MAY. They must agree, and the refusal NAMES
    BOTH VALUES so the reader can see which one is wrong rather than guessing.

    A denial carries no `granted_by` in the ratified entry shape, so only
    `share_out` is checked.
    """
    entries = record.get("share_out")
    if not isinstance(entries, list) or actor is None:
        return
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict):
            continue
        by = entry.get("granted_by")
        if by is None:
            continue
        if str(by).strip() != actor:
            _err(errors,
                 f"share_out[{index}].granted_by: {by!r} is not the designated "
                 f"company-policy actor {actor!r}. A grant recorded under "
                 f"another name means either the wrong person acted or the "
                 f"designation is stale — fix whichever is untrue rather than "
                 f"letting the roster and the designation disagree")


def workspace_root(repo_root: Path) -> Path | None:
    """The workspace holding `.xfactory/notebook-hosting.yaml`, or None.

    WALKED UP FROM THE REPOSITORY RATHER THAN ASSUMED, because this script has
    no root argument and its callers sit in three different shapes: the
    aggregation checkout (the configuration is the aggregation's), a bare clone
    of this repository alone (it is this repository's), and a feature worktree
    under `openxFactory-worktrees/` (it is the aggregation's, two levels up).
    Walking finds all three the way tooling finds a `.git`.

    `scripts/sync-notebooklm-books.py` deliberately does NOT walk: it is handed
    its workspace root and looking outside it would let a real machine's
    configuration reach into a temporary tree.
    """
    here = repo_root.resolve()
    for candidate in (here, *here.parents):
        if (candidate / HOSTING_CONFIG_REL).is_file():
            return candidate
    return None


def hosting_declaration_path(repo_root: Path) -> Path | None:
    """Where this install's live declaration is, or None when UNDECLARED.

    Env var, then the workspace configuration's `declaration_path:`, then
    nothing. THE SHIPPED FIXTURE IS NOT THE LAST STEP — `main()` falls back to
    it only as a FIXTURE to validate, never as a resolution result, and
    `--resolved` refuses that fallback outright.
    """
    named = os.environ.get(HOSTING_ENV, "").strip()
    root = workspace_root(repo_root)
    if named:
        candidate = Path(named).expanduser()
        if candidate.is_absolute():
            return candidate
        return (root or repo_root) / candidate
    if root is None:
        return None
    try:
        config = yaml.safe_load((root / HOSTING_CONFIG_REL).read_text(
            encoding="utf-8"))
    except (OSError, yaml.YAMLError):
        return None
    if not isinstance(config, dict):
        return None
    declared = config.get("declaration_path")
    if not isinstance(declared, str) or not declared.strip():
        return None
    candidate = Path(declared.strip()).expanduser()
    return candidate if candidate.is_absolute() else root / candidate


def _is_example(path: Path) -> bool:
    """True when the record says of itself that it is a fixture.

    Read from the RECORD and never inferred from the path: a copy, a symlink or
    a worktree makes a path comparison unreliable, and the marker is the one
    signal both readers can agree on (OQ-C).
    """
    try:
        record = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError):
        return False
    if not isinstance(record, dict):
        return False
    hosting = record.get("hosting")
    if not isinstance(hosting, dict):
        return False
    return hosting.get("instance") == HOSTING_EXAMPLE_MARKER


def main(argv: list[str]) -> int:
    repo_root = Path(__file__).resolve().parent.parent
    args = [a for a in argv[1:] if a != "--resolved"]
    resolved_only = "--resolved" in argv[1:]

    # PRECEDENCE: an explicit path, then the resolver, then the shipped
    # instance AS A FIXTURE. The third arm is what keeps the record's SHAPE
    # gated in CI after the live record has moved out of this repository; it is
    # not a guess about which install is running.
    if args:
        path, source = Path(args[0]).expanduser(), "the path given"
    else:
        resolved = hosting_declaration_path(repo_root)
        if resolved is not None:
            path, source = resolved, "configuration"
        elif resolved_only:
            print(f"validate-notebook-projection-hosting: nothing is "
                  f"configured — this install has NOT declared a hosting "
                  f"identity, which is a transition state rather than a "
                  f"passing one. Set {HOSTING_CONFIG_REL}'s "
                  f"`declaration_path:` or {HOSTING_ENV}. --resolved "
                  f"deliberately does NOT fall back to "
                  f"{DEFAULT_REL}: that file is a synthetic fixture and "
                  f"validating it would answer a question nobody asked.")
            return 1
        else:
            path, source = repo_root / DEFAULT_REL, "the shipped fixture"

    if not path.is_file():
        print(f"validate-notebook-projection-hosting: {path} not found "
              f"({source}) — this install has NOT declared a hosting identity, "
              f"which is a transition state rather than a passing one")
        return 1

    # A GREEN LINE OVER A FIXTURE IS FALSE EVIDENCE, so `--resolved` refuses one.
    # The sync refuses the same record for the same reason; this arm exists
    # because `--resolved`'s whole job is to be the live record's conformance
    # evidence, and evidence that a fixture conforms proves nothing about the
    # install.
    if resolved_only and _is_example(path):
        print(f"validate-notebook-projection-hosting: {path} carries "
              f"`hosting.instance: {HOSTING_EXAMPLE_MARKER}` — configuration is "
              f"pointing at a SYNTHETIC FIXTURE, not at this install's "
              f"declaration. Refusing: a green line here would be evidence "
              f"about a fixture, and --resolved exists to be evidence about "
              f"the live record. Point {HOSTING_CONFIG_REL}'s "
              f"`declaration_path:` at the real one.")
        return 1

    errors = validate(path)
    for error in errors:
        print(f"{path.name}: {error}")
    print(f"validate-notebook-projection-hosting: {len(errors)} error(s) "
          f"over {path} ({source})")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
