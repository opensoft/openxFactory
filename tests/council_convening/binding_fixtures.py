"""Record builders for the Phase 5 tests: the E10 producer binding, the verified
claims the `identity` oracle carries, and the identity-map states (feature 035,
data-model E10; contracts/conformance-corpus.md § Environment oracles).

Shared by `test_binding.py` (T050) and the binding cases of
`test_validator_cli.py` (T052), so the two describe one well-formed binding.
Every builder returns a fresh value; a test mutates its own copy.

It imports no implementation module, so a test module that uses it still fails
at its own import while the implementation is absent (the tests-first rule).

THE VALUES ARE CORPUS VALUES, NEVER LIVE ONES (plan § Constraints, "No live
values"). The audience, the environments, the workflow files, the repository
ids and the enterprise slug are made up for the corpus. The repository
SPELLINGS are not: the binding mechanism is tested over the frozen identity
fixture, whose one complete row is codexFactory's transfer exactly as the live
map records it, so the former-spelling and case-variant cases need the real
spellings (contracts/conformance-corpus.md § The frozen identity fixture).
"""

from __future__ import annotations

import copy
import datetime
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
FAMILY = REPO_ROOT / "contracts" / "council-convening"
BINDING_SCHEMA = FAMILY / "producer-binding.schema.yaml"
BINDING_TEMPLATE = FAMILY / "producer-binding.template.yaml"
SHARED_DEFINITIONS = FAMILY / "shared-definitions.schema.yaml"
IDENTITY_FIXTURE = FAMILY / "conformance" / "fixtures" / "repository-identity.json"
BINDING_VECTORS = FAMILY / "conformance" / "vectors" / "binding"
LIVE_IDENTITY_MAP = Path("contracts") / "policies" / "repository-identity.yaml"

REPLACEMENT = "xfc-resolved-council-1"

#: The vectors' instant, and the same instant in Unix seconds (JWT `exp`/`nbf`).
EVALUATION_TIME = "2026-10-09T00:00:00Z"
EVALUATION_EPOCH = 1791504000

ISSUER = "https://token.actions.githubusercontent.com"
#: GitHub's documented example slug for an enterprise's unique issuer URL.
ENTERPRISE_ISSUER = ISSUER + "/octocat-inc"
AUDIENCE = "council-convening-corpus-audience"

#: The CALLER: the repository the job runs in, the token's `repository` claim.
CALLER = "opensoft/xFactory"
CALLER_ID = 424242
CALLER_OWNER_ID = 101010

#: The GOVERNED repository, in the frozen fixture's CURRENT spelling, and its
#: former spelling and one non-canonical case variant of each.
GOVERNED = "codeXfactory/codexFactory"
GOVERNED_FORMER = "opensoft/codexFactory"
GOVERNED_CASE_VARIANT = "codexfactory/codexFactory"
GOVERNED_FORMER_CASE_VARIANT = "opensoft/CodexFactory"

#: The fixture's PENDING row. `pending_row_rule`: its `former` is still the only
#: address that exists, so it is no former spelling.
PENDING_FORMER = "opensoft/ExampleFactory"
PENDING_CURRENT = "ExampleOrg/ExampleFactory"

#: The fixture's second PENDING row, whose `former` equals the complete row's
#: CURRENT spelling when ASCII case is ignored, and is not byte-equal to it: the
#: precedence probe (a case-fold collision with a complete row is tested before
#: the pending exemption).
COLLIDING_PENDING_FORMER = "codeXfactory/CodexFactory"
COLLIDING_PENDING_CURRENT = "ExampleOrg/CollidingFactory"

#: The frozen governed revision, a later and an earlier first-parent commit,
#: and a commit off the governed first-parent history.
REVISION = "4" * 40
LATER_REVISION = "6" * 40
EARLIER_REVISION = "3" * 40
OFF_HISTORY = "9" * 40

COMMISSION_WORKFLOW = (
    f"{GOVERNED}/.github/workflows/corpus-commission.yml@refs/heads/main")
SEAT_WORKFLOW = f"{GOVERNED}/.github/workflows/corpus-seat.yml@refs/heads/main"

COMMISSION_SUBJECT = f"repo:{CALLER}:ref:refs/heads/main"


def seat_environment(seat: str = "alpha") -> str:
    """The per-seat GitHub environment of Brett Heap's 025 ruling (A),
    2026-10-09, "Per-seat environments (Recommended)": one environment per seat,
    carried in the OIDC `sub`."""
    return f"corpus-seat-{seat}"


def seat_subject(seat: str = "alpha") -> str:
    """GitHub's default `sub` for a job that references an environment:
    `repo:<owner>/<repo>:environment:<name>`."""
    return f"repo:{CALLER}:environment:{seat_environment(seat)}"


def _broker(**overrides) -> dict:
    broker = {
        "broker_ref": "corpus-broker",
        "capability_verified": True,
        "evidence_ref": "corpus-broker-evidence",
    }
    broker.update(overrides)
    return broker


def commission_binding(**overrides) -> dict:
    """A live E10 binding for the commission job."""
    binding = {
        "schema_version": 1,
        "kind": "xfactory_council_producer_binding",
        "protocol": REPLACEMENT,
        "binding_id": "corpus-commission-binding",
        "principal_kind": "github_oidc_job",
        "issuer": ISSUER,
        "audience": AUDIENCE,
        "caller_repository": CALLER,
        "repository_id": CALLER_ID,
        "subject_claim_keys": ["repo", "context"],
        "subject_template": COMMISSION_SUBJECT,
        "permitted_workflows": [
            {
                "operation": "commission",
                "job_workflow_ref": COMMISSION_WORKFLOW,
                "workflow_revision_rule": "equals_governed_revision",
            },
        ],
        "broker": _broker(),
    }
    binding.update(copy.deepcopy(overrides))
    return binding


def seat_binding(seat: str = "alpha", **overrides) -> dict:
    """A live E10 binding for ONE seat: its own `binding_id` and its own
    per-seat environment in the subject (025 ruling (A))."""
    binding = commission_binding(
        binding_id=f"corpus-seat-{seat}-binding",
        subject_template=seat_subject(seat),
        permitted_workflows=[
            {
                "operation": "seat_execution",
                "job_workflow_ref": SEAT_WORKFLOW,
                "workflow_revision_rule": "on_governed_history_since_revision",
            },
        ],
    )
    binding.update(copy.deepcopy(overrides))
    return binding


def claims_for(binding: dict, *, workflow_sha: str = REVISION,
               job_workflow_ref: str | None = None, **overrides) -> dict:
    """The verified claims a job matching `binding` presents."""
    first = binding["permitted_workflows"][0]
    claims = {
        "iss": binding["issuer"],
        "aud": binding["audience"],
        "sub": binding["subject_template"],
        "iat": EVALUATION_EPOCH - 60,
        "nbf": EVALUATION_EPOCH - 60,
        "exp": EVALUATION_EPOCH + 300,
        "repository": binding["caller_repository"],
        "repository_id": str(binding["repository_id"]),
        "job_workflow_ref": job_workflow_ref or first["job_workflow_ref"],
        "job_workflow_sha": workflow_sha,
    }
    claims.update(overrides)
    return claims


def identity(claims: dict, *, verified: bool = True,
             principal_ref: str = "corpus-commission-binding") -> dict:
    """The `identity` oracle: the one home of verified claims. Under 025's
    ruling (A) the principal reference is the binding id."""
    return {
        "verified": verified,
        "claims": copy.deepcopy(claims),
        "principal": {"principal_kind": "github_oidc_job",
                      "principal_ref": principal_ref},
    }


def governed(repository: str = GOVERNED, revision: str = REVISION) -> dict:
    """The record's `governed` member, as far as E10 step 14 reads it."""
    return {"repository": repository, "revision": revision}


def seat_history(*, repository: str = GOVERNED) -> dict:
    """The `governed_history` oracle for the seat rule: the frozen revision, a
    later and an earlier first-parent commit, and one off the history.
    `at_or_after` lists the governed revisions a commit is at or after, itself
    included."""
    return {
        f"{repository}@{EARLIER_REVISION}": {
            "on_first_parent": True, "at_or_after": [EARLIER_REVISION]},
        f"{repository}@{REVISION}": {
            "on_first_parent": True, "at_or_after": [EARLIER_REVISION, REVISION]},
        f"{repository}@{LATER_REVISION}": {
            "on_first_parent": True,
            "at_or_after": [EARLIER_REVISION, REVISION, LATER_REVISION]},
        f"{repository}@{OFF_HISTORY}": {
            "on_first_parent": False, "at_or_after": []},
    }


def fixture_text() -> str:
    """The frozen identity fixture's map text, read from the corpus."""
    return json.loads(IDENTITY_FIXTURE.read_text(encoding="utf-8"))["text"]


def malformed_row_text() -> str:
    """A map text whose complete row has a null `transferred_on`, which
    `load_transfers` reports as malformed (`field_rules.transfer_state`)."""
    text = fixture_text()
    assert "transferred_on: 2026-09-09" in text
    return text.replace("transferred_on: 2026-09-09", "transferred_on: null", 1)


def identity_oracle(state: str = "text", text: str | None = None) -> dict:
    """The `repository_identity` oracle, in one of its three forms."""
    if state == "text":
        return {"state": "text", "text": fixture_text() if text is None else text}
    return {"state": state}


def write_identity_map(root: Path, text: str | None = None) -> Path:
    """Write a map text at `contracts/policies/repository-identity.yaml` under
    `root`, the fixture's text by default. Returns `root`."""
    path = root / LIVE_IDENTITY_MAP
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(fixture_text() if text is None else text, encoding="utf-8")
    return root


# --- the binding inside admission (E2 steps A1 and A4; T051, T055) -----------

#: The governed repository Phase 2's resolution vectors cite. Admission judges
#: the COMMISSION job's token (data-model E2 step A1), so the workflow an
#: admission vector's binding permits is a commission workflow in that
#: repository, under `equals_governed_revision`.
ADMISSION_GOVERNED = "example-org/governed-rules"


def admission_workflow(repository: str = ADMISSION_GOVERNED) -> str:
    return f"{repository}/.github/workflows/corpus-commission.yml@refs/heads/main"


def admission_binding(repository: str = ADMISSION_GOVERNED, **overrides) -> dict:
    """The commission job's binding, permitting the commission workflow of
    `repository`."""
    binding = commission_binding(permitted_workflows=[{
        "operation": "commission",
        "job_workflow_ref": admission_workflow(repository),
        "workflow_revision_rule": "equals_governed_revision",
    }])
    binding.update(copy.deepcopy(overrides))
    return binding


def epoch_of(instant: str) -> int:
    """A `utc_instant` in Unix seconds, the unit of the JWT `exp`/`nbf` claims."""
    moment = datetime.datetime.strptime(instant, "%Y-%m-%dT%H:%M:%SZ")
    return int(moment.replace(tzinfo=datetime.timezone.utc).timestamp())


def with_passing_binding(vector: dict, *, repository: str | None = None) -> dict:
    """`vector`, an admission vector, made to carry a binding that passes E2
    steps A1 and A4 for its own record: the commission job's verified claims
    name the record's governed repository (or `repository`) and its governed
    revision, and the map is the frozen fixture's text. Mutates and returns
    `vector`; members spelled with `$parts` are left as they are. The token's
    window is open at the vector's own `evaluation_time`.

    A record with no readable `governed` member (one refused at step 1 or 2,
    before A1 runs) gets the corpus's governed repository and revision."""
    record = vector["inputs"]["record"]
    provenance = record.get("required_seats_provenance") if isinstance(record, dict) else None
    member = provenance.get("governed") if isinstance(provenance, dict) else None
    if not isinstance(member, dict):
        member = {}
    bound = admission_binding(repository or member.get("repository", ADMISSION_GOVERNED))
    vector["inputs"]["binding"] = bound
    vector["inputs"]["operation"] = "commission"
    vector.setdefault("environment", {})
    now = epoch_of(vector.get("evaluation_time", EVALUATION_TIME))
    vector["environment"]["identity"] = identity(claims_for(
        bound, workflow_sha=member.get("revision", REVISION),
        iat=now - 60, nbf=now - 60, exp=now + 300))
    vector["environment"]["repository_identity"] = identity_oracle()
    return vector
