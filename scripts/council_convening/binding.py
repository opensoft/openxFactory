"""The producer workflow binding, data-model E10 (feature 035, Phase 5, T054).

A binding names one producer principal: the OIDC issuer and audience its token
must carry, the repository its job runs in, the exact subject its token's `sub`
must equal, and the reusable workflows it may run per operation, each with the
ruled revision rule (`producer-binding.schema.yaml`). This module judges a
binding, and a verified token against it, in E10's fourteen-step order. The
first failing check names the outcome (research R21).

* Steps 1 to 6, `check_offline`, judge the instance alone: shape, wildcards,
  the issuer form, the repository identity map, and the subject template.
  `scripts/validate-council-convening.py check` runs them offline.
* Steps 7 to 13, `check_claims`, judge the `identity` oracle's verified claims.
* Step 14, `check_workflow_revision`, applies the matched entry's
  `workflow_revision_rule` to the record's `governed` member.

At admission the consumer runs steps 1 to 13 as E2 step A1, right after the
record's shape check, and step 14 as E2 step A4, after E2 step 5 has checked
the `governed` member it reads (data-model E2). So steps 1 to 13 never read
`governed`.

THE IDENTITY MAP IS READ THROUGH `load_transfers` AND NOTHING ELSE. There is no
second transfer map. `load_transfers` (`scripts/estate_inventory.py`) returns an
empty map for an absent or unreadable file, which is right for its own reports
and fails open here, so `load_identity_map` first confirms the map exists,
reads, and parses under the same strict loader into a well-formed map, and
refuses `repository_identity_unavailable` otherwise, and when `load_transfers`
reports any malformed row. A well-formed map with no transfer rows is valid.

THE CORPUS NEVER READS THE LIVE MAP (round 7, R7-M1). A vector carries its map
in the `repository_identity` oracle; `materialize_identity` writes that oracle
under a temporary root, and `evaluate_vector` reads it there with the same
reader.

Brett Heap's rulings encoded here, 2026-10-08: OPEN-2, "Consumer's runtime
config (Recommended)" (the instance lives in the consumer's configuration);
OPEN-3, "History + unchanged rule file (Recommended)", with follow-up 2,
"job_workflow_ref's repo (Recommended)", and follow-up 3, "At or after the
frozen rev (Recommended)" (step 14).

ALWAYS IMPORT THIS MODULE AS `scripts.council_convening.binding`.
"""

from __future__ import annotations

import datetime
import functools
import re
import string
import sys
import tempfile
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parents[1]
if str(_SCRIPTS) not in sys.path:
    # APPENDED, never prepended, so no name another tree resolves is shadowed.
    # `estate_inventory` and the strict loader it uses are top-level modules of
    # `scripts/`, which is how every other reader imports them.
    sys.path.append(str(_SCRIPTS))

import estate_inventory  # noqa: E402
import frontmatter_strict as fm  # noqa: E402

from . import records  # noqa: E402
from .records import Refused  # noqa: E402

SCHEMA_PATH = records.REPO_ROOT / records.FAMILY_REL / "producer-binding.schema.yaml"

#: The identity map's repository-relative path, as `load_transfers` reads it.
IDENTITY_MAP = estate_inventory.TRANSFER_MAP

#: The ruled, closed `workflow_revision_rule`, one value per operation (OPEN-3;
#: follow-up 3). Any other pairing is `binding_malformed`, by the schema.
WORKFLOW_REVISION_RULES = {
    "commission": "equals_governed_revision",
    "seat_execution": "on_governed_history_since_revision",
}
OPERATIONS = tuple(WORKFLOW_REVISION_RULES)

#: GitHub's issuer, and the form of an enterprise's unique issuer URL,
#: `https://token.actions.githubusercontent.com/<enterprise-slug>`. GitHub
#: documents the form, with the example slug `octocat-inc`, and states no
#: grammar for the slug; this module accepts one path segment of lowercase
#: letters, digits and inner hyphens.
GITHUB_ISSUER = "https://token.actions.githubusercontent.com"
_ENTERPRISE_SLUG = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")

#: The closed subject claim keys, mirrored from the schema's enumeration (a test
#: holds the two equal). Source: GitHub's "OpenID Connect reference",
#: https://docs.github.com/en/actions/reference/security/oidc, read 2026-10-09.
SUBJECT_CLAIM_KEYS = (
    "repo", "context",
    "actor", "actor_id", "base_ref", "check_run_id", "enterprise",
    "enterprise_id", "environment", "event_name", "head_ref",
    "job_workflow_ref", "job_workflow_sha", "ref", "ref_type", "repository",
    "repository_id", "repository_owner", "repository_owner_id",
    "repository_visibility", "run_attempt", "run_id", "run_number",
    "runner_environment", "workflow", "workflow_ref", "workflow_sha",
)

#: The refusal codes this phase adds to `refusal_code` (data-model § Refusal
#: vocabulary). `binding_unresolved` and `broker_capability_insufficient` are
#: Phase 4's, where their first triggers are (R5-M2).
PHASE_5_REFUSAL_CODES = (
    "binding_malformed",
    "claims_unverified",
    "claims_expired",
    "issuer_mismatch",
    "audience_mismatch",
    "binding_wildcard",
    "repository_identity_unavailable",
    "repository_identity_former",
    "repository_identity_mismatch",
    "subject_template_mismatch",
    "subject_workflow_conflation",
    "workflow_not_permitted",
    "workflow_revision_ungoverned",
)

#: Steps 1 to 6, in order: what `check` runs offline.
OFFLINE_STEPS = (
    "binding_malformed", "binding_wildcard", "issuer_mismatch",
    "repository_identity_unavailable", "repository_identity_former",
    "subject_workflow_conflation", "subject_template_mismatch")

#: Steps 7 to 14, in order: the rules `check` reports as not offline-checkable,
#: because they need the verified claims and the governed history.
CLAIM_RULES = (
    "claims_unverified", "claims_expired", "issuer_mismatch",
    "audience_mismatch", "subject_template_mismatch",
    "repository_identity_mismatch", "workflow_not_permitted",
    "workflow_revision_ungoverned")

_NAME = r"[A-Za-z0-9_.-]+"
_DECIMAL_ID = r"[1-9][0-9]*"
_REPOSITORY = re.compile(rf"({_NAME})/({_NAME})")
#: GitHub's immutable `repo` segment, `<owner>@<owner-id>/<repo>@<repo-id>`,
#: used by repositories created, renamed or transferred after 2026-07-15.
_IMMUTABLE_REPOSITORY = re.compile(
    rf"({_NAME})@({_DECIMAL_ID})/({_NAME})@({_DECIMAL_ID})")
#: The ref may carry `@`: git forbids only `@{` and a lone `@` in a ref name
#: (git-check-ref-format), so `refs/heads/rel@2` is a branch. The file name
#: carries none, so the first `@` after the path is the separator.
_WORKFLOW_REF = re.compile(
    rf"(?P<owner>{_NAME})/(?P<name>{_NAME})/\.github/workflows/"
    r"(?P<file>[^/@:\s\x00-\x1f\x7f]+)@(?P<ref>[^:\s\x00-\x1f\x7f]+)")
_FULL_SHA = re.compile(r"[0-9a-f]{40}")
_DECIMAL = re.compile(_DECIMAL_ID)
#: One `sub` element value: no `:` (GitHub writes one inside a value as `%3A`)
#: and no control character. READING: at least one character, so a customized
#: template whose last element is empty (`head_ref:` on an event with no head
#: ref) does not parse, and is `subject_template_mismatch`. A binding is per
#: principal and per job, so such a job needs a template without that key.
_VALUE = re.compile(r"[^:\x00-\x1f\x7f-\x9f]+")
_UTC_INSTANT = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z")
_FOLD = str.maketrans(string.ascii_uppercase, string.ascii_lowercase)

#: Bytes that are not UTF-8: the `unreadable` state of the identity oracle.
_UNREADABLE_BYTES = b"\xff\xfe\xfd not utf-8\n"


def _refuse(code: str, member: str) -> Refused:
    # A member NAME, never a value: a refusal message echoes nothing a secret
    # detector could match (T017).
    return Refused(code, member)


# --- the shape (step 1) --------------------------------------------------------


#: The schema's `$id`, the reference `records.SchemaSet` resolves it by.
SCHEMA_REF = records.ID_BASE + SCHEMA_PATH.name


@functools.lru_cache(maxsize=1)
def _default_schemas() -> records.SchemaSet:
    return records.load_schemas()


def schema_errors(binding: object, schemas: records.SchemaSet | None = None) -> list[str]:
    """Every way `binding` fails `producer-binding.schema.yaml`, through the
    family's one schema registry (`records.load_schemas`, whole-match patterns),
    as the failing paths, never a value. Empty when the shape holds, which a
    stub's shape does: refusing a stub as live is step 1's second half."""
    schemas = schemas if schemas is not None else _default_schemas()
    return ["/".join(str(p) for p in error.absolute_path) or "<record>"
            for error in schemas.errors(SCHEMA_REF, binding)]


# --- the identity map (step 4) -------------------------------------------------


def _ascii_fold(value: str) -> str:
    return value.translate(_FOLD)


@dataclass(frozen=True)
class IdentityMap:
    """The complete transfers `load_transfers` resolves, `{former: current}`,
    and the spellings the map's PENDING rows list, which it does not resolve."""

    transfers: Mapping[str, str]
    pending: frozenset = frozenset()

    def is_former(self, spelling: str) -> bool:
        """True for a former spelling, or for a non-canonical case variant: a
        spelling equal to a listed spelling when ASCII case is ignored, but not
        byte-equal to it (research.md R10; the map's `owner_case`, made
        mechanical). Listed means a complete row's `former` or `current`, or a
        pending row's `former` or `current` (E10 step 4, read literally: "a
        listed spelling").

        THE ORDER IS THE RULE. A complete row's own spellings are tested
        FIRST: its `former` is refused and its `current` is current. Then a
        case-fold collision with any complete-row spelling is refused, BEFORE
        the pending exemption, so a pending row cannot shadow a complete row's
        case variant (the delta review's probe: a pending row spelled
        `codeXfactory/CodexFactory` beside the complete current
        `codeXfactory/codexFactory`). Only then is a pending row's spelling,
        byte-equal, exempt: `load_transfers` does not resolve the row, because
        its `former` is still the only address (`pending_row_rule`). Last, a
        case variant of a pending spelling is refused. Any spelling the map
        does not list is current."""
        formers = set(self.transfers)
        currents = set(self.transfers.values())
        if spelling in formers:
            return True
        if spelling in currents:
            return False
        folded = _ascii_fold(spelling)
        if any(_ascii_fold(listed) == folded for listed in formers | currents):
            return True
        if spelling in self.pending:
            return False
        return any(_ascii_fold(listed) == folded for listed in self.pending)

def load_identity_map(root: Path) -> IdentityMap:
    """The identity map under `root`, read through `load_transfers`, or
    `repository_identity_unavailable`.

    `load_transfers` takes an absent or unreadable map for an empty one. This
    check runs first: the file must exist with no symlink on its path (the
    reader's own `_unescaped` rule), decode as UTF-8, parse under the same
    strict loader, and be a well-formed map, meaning a mapping with
    `schema_version: 1`, `kind: repository_identity` and a `transfers` list
    whose rows are mappings with string `former` and `current`. Then any row
    `load_transfers` reports as malformed refuses too.
    """
    unavailable = _refuse("repository_identity_unavailable", "repository_identity")
    path = estate_inventory._unescaped(root, IDENTITY_MAP)
    if path is None or not path.is_file():
        raise unavailable
    try:
        document = fm.strict_load(path.read_text(encoding="utf-8"),
                                  what=str(IDENTITY_MAP))
    except (OSError, UnicodeDecodeError, fm.StrictFrontMatterError, ValueError):
        raise unavailable from None
    if not isinstance(document, dict):
        raise unavailable
    version = document.get("schema_version")
    rows = document.get("transfers")
    if (type(version) is not int or version != 1
            or document.get("kind") != "repository_identity"
            or not isinstance(rows, list)):
        raise unavailable
    for row in rows:
        if not (isinstance(row, dict) and isinstance(row.get("former"), str)
                and isinstance(row.get("current"), str)):
            raise unavailable
    transfers, malformed = estate_inventory.load_transfers(root)
    if malformed:
        raise unavailable
    # Every row `load_transfers` did not refuse and did not resolve is a lawful
    # pending row (its `pending_row_rule`); its spellings are listed spellings.
    pending = frozenset(
        spelling for row in rows if row.get("transfer_state") == "pending"
        for spelling in (row["former"], row["current"]))
    return IdentityMap(dict(transfers), pending)


def materialize_identity(oracle: object, root: Path) -> Path:
    """Write the `repository_identity` oracle at the map's path under `root`
    and return `root`, so the reader judges it there (conformance-corpus §
    Environment oracles): `text` writes the exact text, `absent` writes nothing,
    and `unreadable` writes bytes that do not decode. A malformed oracle is a
    harness error (`ValueError`), never a refusal."""
    if not isinstance(oracle, Mapping):
        raise ValueError("repository_identity oracle is not an object")
    state = oracle.get("state")
    if state == "text":
        if set(oracle) != {"state", "text"} or not isinstance(oracle["text"], str):
            raise ValueError("repository_identity text oracle is malformed")
    elif state in ("absent", "unreadable"):
        if set(oracle) != {"state"}:
            raise ValueError(f"repository_identity {state} oracle carries members")
    else:
        raise ValueError("repository_identity oracle has an unknown state")
    root.mkdir(parents=True, exist_ok=True)
    path = root / IDENTITY_MAP
    if state == "absent":
        return root
    path.parent.mkdir(parents=True, exist_ok=True)
    if state == "text":
        path.write_bytes(oracle["text"].encode("utf-8"))
    else:
        path.write_bytes(_UNREADABLE_BYTES)
    return root


# --- the grammars (steps 4 to 6, 13 and 14) ------------------------------------


@dataclass(frozen=True)
class WorkflowRef:
    repository: str
    file: str
    ref: str


def parse_workflow_ref(value: object) -> WorkflowRef | None:
    """`<owner>/<repo>/.github/workflows/<file>@<ref>`, matched whole, or None."""
    if not isinstance(value, str):
        return None
    match = _WORKFLOW_REF.fullmatch(value)
    if match is None:
        return None
    return WorkflowRef(f"{match['owner']}/{match['name']}", match["file"],
                       match["ref"])


def _ref_repository(ref: str) -> str | None:
    """`<owner>/<repo>` from a permitted ref's first two `/` segments, or None
    when it has fewer than two."""
    segments = ref.split("/", 2)
    if len(segments) < 2 or not segments[0] or not segments[1]:
        return None
    return f"{segments[0]}/{segments[1]}"


def is_bare_workflow_reference(template: object) -> bool:
    """Step 5: the template IS a workflow reference, with no `key:` element.
    Judged by meaning, not substring: a template that carries the
    `job_workflow_ref` claim key through GitHub's subject customization has a
    `key:` element and is legal."""
    return (isinstance(template, str) and ":" not in template
            and parse_workflow_ref(template) is not None)


def _value_ok(key: str, value: str) -> bool:
    if not _VALUE.fullmatch(value):
        return False
    if key == "repo":
        return bool(_REPOSITORY.fullmatch(value)
                    or _IMMUTABLE_REPOSITORY.fullmatch(value))
    if key == "repository":
        return bool(_REPOSITORY.fullmatch(value))
    if key in ("repository_id", "repository_owner_id", "actor_id"):
        return bool(_DECIMAL.fullmatch(value))
    if key == "job_workflow_ref":
        return parse_workflow_ref(value) is not None
    return True


def parse_subject(template: object, keys: Sequence[str]) -> tuple | None:
    """Parse an OIDC `sub` into `((key, value), ...)` in `keys` order, under
    GitHub's documented grammar, or None.

    Elements are joined by `:`, and GitHub writes a `:` inside a value as
    `%3A`, so the split is exact. `repo` is `repo:<owner>/<repo>`, or GitHub's
    immutable `repo:<owner>@<owner-id>/<repo>@<repo-id>`. `context` is one of
    `environment:<name>`, `pull_request` or `ref:<ref>`, returned joined. Every
    other key is `<key>:<value>`. Every key must yield exactly one element, and
    nothing may follow the last.
    """
    if not isinstance(template, str) or not keys:
        return None
    tokens = template.split(":")
    position = 0
    elements = []
    for key in keys:
        if position >= len(tokens):
            return None
        head = tokens[position]
        if key == "context":
            if head == "pull_request":
                elements.append(("context", head))
                position += 1
                continue
            if head not in ("environment", "ref") or position + 1 >= len(tokens):
                return None
            value = tokens[position + 1]
            if not _VALUE.fullmatch(value):
                return None
            elements.append(("context", f"{head}:{value}"))
            position += 2
            continue
        if head != key or position + 1 >= len(tokens):
            return None
        value = tokens[position + 1]
        if not _value_ok(key, value):
            return None
        elements.append((key, value))
        position += 2
    if position != len(tokens):
        return None
    return tuple(elements)


def _names_the_binding_repository(elements: tuple, binding: Mapping) -> bool:
    """Step 6's second half. The template must carry a repository element
    (`repo`, `repository` or `repository_id`), and each one it carries must
    name `caller_repository` or `repository_id`, byte for byte."""
    caller = binding["caller_repository"]
    repository_id = str(binding["repository_id"])
    found = False
    for key, value in elements:
        if key == "repo":
            immutable = _IMMUTABLE_REPOSITORY.fullmatch(value)
            if immutable:
                named = f"{immutable[1]}/{immutable[3]}"
                if named != caller or immutable[4] != repository_id:
                    return False
            elif value != caller:
                return False
            found = True
        elif key == "repository":
            if value != caller:
                return False
            found = True
        elif key == "repository_id":
            if value != repository_id:
                return False
            found = True
    return found


# --- steps 1 to 6 ----------------------------------------------------------------


def check_offline(binding: object, *, identity_root: Path,
                  schemas: records.SchemaSet | None = None) -> None:
    """E10 steps 1 to 6 on the instance alone, reading the identity map under
    `identity_root`. Raises `Refused` with the first failing step's code."""
    # 1. The shape, then a stub presented as live.
    if schema_errors(binding, schemas):
        raise _refuse("binding_malformed", "binding")
    if "instantiation_stub" in binding:
        raise _refuse("binding_malformed", "instantiation_stub")
    workflows = [entry["job_workflow_ref"] for entry in binding["permitted_workflows"]]

    # 2. A wildcard in any member that could carry one.
    for member, value in (("issuer", binding["issuer"]),
                          ("audience", binding["audience"]),
                          ("subject_template", binding["subject_template"]),
                          *(("permitted_workflows", ref) for ref in workflows)):
        if "*" in value:
            raise _refuse("binding_wildcard", member)

    # 3. The issuer form.
    issuer = binding["issuer"]
    if issuer != GITHUB_ISSUER:
        prefix = GITHUB_ISSUER + "/"
        if not (issuer.startswith(prefix)
                and _ENTERPRISE_SLUG.fullmatch(issuer[len(prefix):])):
            raise _refuse("issuer_mismatch", "issuer")

    # 4. The identity map, then former spellings and case variants.
    identity_map = load_identity_map(identity_root)
    if identity_map.is_former(binding["caller_repository"]):
        raise _refuse("repository_identity_former", "caller_repository")
    for ref in workflows:
        # The repository is judged from the ref's first two `/` segments, whether
        # or not the whole ref parses: a ref this grammar does not read still
        # names its repository there, and a former spelling there fails closed.
        repository = _ref_repository(ref)
        if repository is not None and identity_map.is_former(repository):
            raise _refuse("repository_identity_former", "permitted_workflows")

    # 5. Conflation, before the parse that would also refuse it (R3-H1).
    template = binding["subject_template"]
    if is_bare_workflow_reference(template):
        raise _refuse("subject_workflow_conflation", "subject_template")

    # 6. The template parses, and names the binding's repository.
    elements = parse_subject(template, binding["subject_claim_keys"])
    if elements is None or not _names_the_binding_repository(elements, binding):
        raise _refuse("subject_template_mismatch", "subject_template")


# --- steps 7 to 13 ---------------------------------------------------------------


def _epoch(instant: str) -> int:
    if not isinstance(instant, str) or not _UTC_INSTANT.fullmatch(instant):
        raise ValueError("evaluation_time is not a utc_instant")
    moment = datetime.datetime.strptime(instant, "%Y-%m-%dT%H:%M:%SZ")
    return int(moment.replace(tzinfo=datetime.timezone.utc).timestamp())


def _is_integer(value: object) -> bool:
    return type(value) is int


def check_claims(binding: Mapping, *, operation: str, identity: object,
                 evaluation_time: str) -> dict:
    """E10 steps 7 to 13 on the `identity` oracle, for a binding that passed
    steps 1 to 6. Returns the matched `permitted_workflows` entry. Never reads
    the record's `governed` member, so it runs as E2 step A1."""
    if operation not in OPERATIONS:
        raise ValueError("operation is not one of " + ", ".join(OPERATIONS))
    now = _epoch(evaluation_time)

    # 7. Claims from a decoded assertion whose signature was not verified.
    if not isinstance(identity, Mapping) or identity.get("verified") is not True:
        raise _refuse("claims_unverified", "identity")
    claims = identity.get("claims")
    if not isinstance(claims, Mapping):
        raise _refuse("claims_unverified", "identity")

    # 8. The validity window: `exp` at or before the instant, or `nbf` after it.
    #    A token with no integer `exp` has no window, and fails closed.
    expiry = claims.get("exp")
    if not _is_integer(expiry) or expiry <= now:
        raise _refuse("claims_expired", "exp")
    if "nbf" in claims:
        not_before = claims["nbf"]
        if not _is_integer(not_before) or not_before > now:
            raise _refuse("claims_expired", "nbf")

    # 9 to 11. The verified issuer, audience and subject, exactly. An `aud` that
    # is a list is not exactly the binding's audience.
    if claims.get("iss") != binding["issuer"]:
        raise _refuse("issuer_mismatch", "iss")
    if claims.get("aud") != binding["audience"]:
        raise _refuse("audience_mismatch", "aud")
    if claims.get("sub") != binding["subject_template"]:
        raise _refuse("subject_template_mismatch", "sub")

    # 12. The verified repository and its immutable id. GitHub issues
    #     `repository_id` as a decimal string.
    if claims.get("repository") != binding["caller_repository"]:
        raise _refuse("repository_identity_mismatch", "repository")
    if claims.get("repository_id") != str(binding["repository_id"]):
        raise _refuse("repository_identity_mismatch", "repository_id")

    # 13. The verified `job_workflow_ref`, never `sub`, listed for the operation.
    ref = claims.get("job_workflow_ref")
    for entry in binding["permitted_workflows"]:
        if entry["operation"] == operation and entry["job_workflow_ref"] == ref:
            return dict(entry)
    raise _refuse("workflow_not_permitted", "job_workflow_ref")


# --- step 14 ---------------------------------------------------------------------


def check_workflow_revision(entry: Mapping, *, identity: Mapping,
                            governed: Mapping, governed_history: object) -> None:
    """E10 step 14: the verified `job_workflow_sha` under the matched entry's
    `workflow_revision_rule`, read against the record's `governed` member (for
    a seat job, the snapshot's frozen one). Runs as E2 step A4.

    The repository compared is the one the verified `job_workflow_ref` names,
    whose commit `job_workflow_sha` is, never the caller (follow-up 2). So a
    permitted workflow outside the governed repository fails closed here.
    """
    claims = identity["claims"]
    parsed = parse_workflow_ref(claims.get("job_workflow_ref"))
    sha = claims.get("job_workflow_sha")
    repository = governed.get("repository")
    revision = governed.get("revision")
    if (parsed is None or parsed.repository != repository
            or not isinstance(sha, str) or not _FULL_SHA.fullmatch(sha)):
        raise _refuse("workflow_revision_ungoverned", "job_workflow_sha")
    rule = entry["workflow_revision_rule"]
    if rule == "equals_governed_revision":
        if sha != revision:
            raise _refuse("workflow_revision_ungoverned", "job_workflow_sha")
        return
    if rule == "on_governed_history_since_revision":
        # Follow-up 3: on the governed first-parent history, at or after the
        # frozen revision. `at_or_after` lists the governed revisions a commit
        # is at or after, itself included. A commit the history does not know
        # is not on it.
        record = (governed_history.get(f"{repository}@{sha}")
                  if isinstance(governed_history, Mapping) else None)
        after = record.get("at_or_after") if isinstance(record, Mapping) else None
        if (not isinstance(record, Mapping)
                or record.get("on_first_parent") is not True
                or not isinstance(after, list) or revision not in after):
            raise _refuse("workflow_revision_ungoverned", "job_workflow_sha")
        return
    raise ValueError("workflow_revision_rule is not a ruled value")


# --- the whole order ----------------------------------------------------------


def check_binding(binding: object, *, operation: str, identity: object,
                  governed: Mapping, governed_history: object = None,
                  evaluation_time: str, identity_root: Path,
                  schemas: records.SchemaSet | None = None) -> dict:
    """E10 steps 1 to 14, the `binding` boundary. Returns the matched
    permitted workflow; raises `Refused` with the first failing step's code."""
    check_offline(binding, identity_root=identity_root, schemas=schemas)
    entry = check_claims(binding, operation=operation, identity=identity,
                         evaluation_time=evaluation_time)
    check_workflow_revision(entry, identity=identity, governed=governed,
                            governed_history=governed_history)
    return entry


def evaluate_vector(vector: Mapping,
                    schemas: records.SchemaSet | None = None) -> tuple[str, str | None]:
    """Adjudicate one `binding` vector: `("accept", None)` or
    `("refuse", <code>)`. The map is the vector's own `repository_identity`
    oracle, materialized under a temporary root, never the live file.

    An oracle the order READS and the vector does not carry is a harness error
    (`ValueError`), never a refusal, as at admission: `identity` once steps 1
    to 6 pass, and `governed_history` for a seat job's step 14."""
    inputs = vector["inputs"]
    environment = vector.get("environment", {})
    with tempfile.TemporaryDirectory(prefix="council-convening-identity-") as tmp:
        root = materialize_identity(environment["repository_identity"],
                                    Path(tmp) / "root")
        try:
            check_offline(inputs["binding"], identity_root=root, schemas=schemas)
            if "identity" not in environment:
                raise ValueError("the vector carries no `identity` oracle, which "
                                 "E10 step 7 reads")
            entry = check_claims(inputs["binding"], operation=inputs["operation"],
                                 identity=environment["identity"],
                                 evaluation_time=vector["evaluation_time"])
            if (entry["workflow_revision_rule"] == "on_governed_history_since_revision"
                    and "governed_history" not in environment):
                raise ValueError("the vector carries no `governed_history` oracle, "
                                 "which E10 step 14 reads for a seat job")
            check_workflow_revision(entry, identity=environment["identity"],
                                    governed=inputs["governed"],
                                    governed_history=environment.get("governed_history"))
        except Refused as refused:
            return "refuse", refused.code
    return "accept", None
