from __future__ import annotations

from .hosting_paths import HOSTING_CONFIG_REL, HOSTING_ENV

HOSTING_EXAMPLE_MARKER = "example"
_MIGRATION_STATES = (None, "", "pending", "complete")
_NON_USER_MARKERS = (".iam.gserviceaccount.com", ".gserviceaccount.com")


def refuse_unusable_declaration(
    declared: dict[str, str], where: str | None = None
) -> None:
    found = where or "the resolved hosting declaration"
    if not declared:
        raise SystemExit(
            f"hosting: {found} EXISTS but no declaration could be read from it. The sync reads the `hosting:` block's own two-space scalars; flow style, other indentation or tabs parse as valid YAML for the validator and as nothing here. Refusing rather than running unbound — an unreadable declaration is not an absent one. Re-indent it to match examples/notebook-projection-hosting.yaml."
        )
    if declared.get("instance") == HOSTING_EXAMPLE_MARKER:
        raise SystemExit(
            f"hosting: {found} is the SHIPPED SYNTHETIC EXAMPLE — it carries `hosting.instance: {HOSTING_EXAMPLE_MARKER}` and every identity in it is fictional. Refusing rather than binding: a fixture is no install's declaration, and binding to one would write a governed projection into an account nobody declared.\n  point configuration at this install's OWN declaration:\n    {HOSTING_CONFIG_REL}  ->  declaration_path: <path to it>\n  or, for one run:   {HOSTING_ENV}=<path to it>\n  the live record is not in this repository; see docs/lifecycle-notebook-projection.md § The declaration."
        )
    case = declared.get("case")
    account = declared.get("account", "")
    state = declared.get("migration_state")
    if state not in _MIGRATION_STATES:
        raise SystemExit(
            f"hosting: migration.state is {state!r}; it is 'pending', 'complete', or absent. An unrecognized state would otherwise bind the run to the DECLARED profile while the books are still in the previous account — a premature migration under --apply."
        )
    if state == "pending" and (not declared.get("migration_from_nlm_profile")):
        raise SystemExit(
            "hosting: a PENDING migration must name migration.from_nlm_profile — the sync binds there until the books move, and cannot bind to a profile nobody named."
        )
    if not declared.get("nlm_profile"):
        raise SystemExit(
            f"hosting: {found} names no top-level nlm_profile. It is required in every state: it is what the run binds to once a migration completes."
        )
    if case not in ("operator_hosted", "self_hosted"):
        raise SystemExit(
            f"hosting: {found} declares case {case!r}; an install declares exactly one of operator_hosted or self_hosted"
        )
    if "@" not in account:
        raise SystemExit(f"hosting: {found} names no usable account address")
    if any(marker in account for marker in _NON_USER_MARKERS):
        raise SystemExit(
            f"hosting: {account} is a service account. The hosting identity MUST be a Google USER account — NotebookLM has no API and a service account cannot drive its consumer web UI, so this declaration could never work"
        )
    if case != "operator_hosted":
        return
    if declared.get("account_type") != "google_workspace_user":
        raise SystemExit(
            f"hosting: {account} is declared operator-hosted but its account_type is {declared.get('account_type')!r}. The operator-hosted case requires a google_workspace_user: a consumer account keeps a personal recovery path and no admin console, which is what this case exists to remove"
        )
    domain = declared.get("domain", "")
    if not domain:
        raise SystemExit(
            "hosting: an operator-hosted declaration must name the domain the operating party administers"
        )
    if not account.lower().endswith("@" + domain.lower()):
        raise SystemExit(
            f"hosting: {account} is not in the declared domain {domain} — the operating party must administer the account it declares"
        )
