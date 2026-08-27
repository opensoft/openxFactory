"""MODEL INTAKE: what a human ADDS, and the separate act that APPROVES it
(add-doxchat-model-intake sections 2 and 3).

THE ONE DISTINCTION THIS MODULE EXISTS TO HOLD. Before it, "approved" was not a
record. It was the conjunction of three runtime facts — the entry sits in the
`ModelCatalog` the install handed to `model_port_factory`, its `available` flag
is true, and the console passed the `session` local-human verdict. That is
defensible while the only way to add a model is to edit the settings document,
because whoever can do that IS the operator by definition. A WIZARD BREAKS THE
IMPLICATION: if completing an intake flow set `available`, then supplying a
payment credential would be the same act as approving a provider to process
governed corpus material, and the placeholder the human is looking at already
says "approved model". So intake PROPOSES and a recorded human act APPROVES, and
this module is where the proposal lives until that record exists.

WHAT IS *NOT* IN THIS MODULE, deliberately: the credential, the broker
invocation, the minted token, and every provider transport. Those are
`doxbench_provider`'s, the ONE module this repository permits to hold them. This
one holds records and a file. It reaches no network, spawns no process, and
never sees a credential — which is why it is safe for it to be the surface a
browser talks to.

WHAT IT DOES NOT WIDEN, also deliberately: the BINDING's closed nine-field
record (`doxbench_binding.BINDING_FIELDS`) and the CATALOG entry's closed
seven-field public shape (`doxbench_model.ModelCatalogEntry`). Proposed-versus-
approved is a SERVER-SIDE distinction and a pending declaration is simply not in
the catalog, so neither released shape gains a field and neither needs a release
act. The declaration is a SECOND record beside the binding, not a tenth field on
it.

WHY PENDING-NESS IS A DECLARED FACT AND NOT A DEFAULT. A binding this document
says nothing about is UNAFFECTED: it resolves exactly as it resolved before this
change, byte for byte, because a binding declared by hand in the settings file
was declared by the operator, and the operator is who approval is a record of.
Only a declaration THIS flow wrote carries a `pending` status, and only that
status suppresses. Inverting the rule — every binding pending until approved —
would have retroactively unapproved every install that already works, which is
the one thing a change adding a safeguard must not do.

STDLIB AT IMPORT TIME, and `yaml` only when a document is actually parsed or
written, for exactly the reason `doxbench_binding` gives: THE LEAN HOSTED IMAGE
HAS NO PyYAML and both entrypoints resolve their model port through this family
at startup. A store with no document reads as empty without touching the parser.
"""

from __future__ import annotations

import dataclasses
from collections.abc import Iterable, Mapping
from datetime import datetime, timedelta, timezone
from pathlib import Path

from ideation_dashboard import doxbench_binding as binding_mod

# ---------------------------------------------------------------------------
# the record's identity (the workspace rule: every YAML carries both)
# ---------------------------------------------------------------------------

#: The stored document's `schema_version`.
SCHEMA_VERSION = 1

#: The stored document's `kind` — the declarations this install has made.
DECLARATIONS_KIND = "model-declarations"

#: One declaration's own `kind`, stamped on each entry so a record lifted out of
#: the document still says what it is.
DECLARATION_KIND = "model-declaration"

#: The broker block's own `kind`. The block names a PROGRAM and its fixed
#: leading arguments and nothing else: no operation, no flag, and no credential.
BROKER_KIND = "model-credential-broker"

# ---------------------------------------------------------------------------
# the closed vocabularies
# ---------------------------------------------------------------------------

#: A declaration this flow wrote that no human has approved yet. It contributes
#: NO available catalog entry and is disclosed to the human as pending.
STATUS_PENDING = "pending"

#: A declaration a recorded human act approved. The gate-action record naming it
#: exists on disk before this status is ever written.
STATUS_APPROVED = "approved"

#: CLOSED, for the same reason every other vocabulary in this family is: a
#: free-text status riding a record that neither declares nor forbids it is
#: unenforceable and invisible to every consumer.
STATUSES: tuple[str, ...] = (STATUS_PENDING, STATUS_APPROVED)

#: The install this approval was made on is a single-operator loopback console:
#: one human, their own subscription, their own corpus.
POSTURE_SINGLE_OPERATOR = "single-operator"

#: The install is a tenant or shared one, or the turn will process another
#: party's material.
POSTURE_SHARED = "shared"

#: CLOSED. Brett's OQ-3 ruling of 2026-08-21 splits BY INSTALL, so the record
#: has to state which install it was made on — a record that did not could not be
#: read back against the rule it was made under.
POSTURES: tuple[str, ...] = (POSTURE_SINGLE_OPERATOR, POSTURE_SHARED)

#: The gate-action `action` this flow's approval writes. ONE additive member on
#: the released `gate-action-record.schema.yaml` enum (contract-v1.45); reusing
#: an existing member would misname a governance record, which is the failure
#: mode `add-doxbench-editing-phase-b` already hit with `share-session` and
#: declined to take.
GATE_ACTION_APPROVE_MODEL = "approve-model"

#: The record block that gate action carries: the accountability
#: `credential-contracts` already demands of an issued grant. Spelled here, on
#: the module that builds it, so the schema and the producer cannot drift into
#: two field lists.
APPROVAL_FIELDS: tuple[str, ...] = (
    "issued_by", "approved_by", "expires_at", "audit_ref", "install_posture")

#: The exact, ordered field list a declaration carries. Nothing else may appear
#: in a stored record and nothing else appears in a read-back. NO CREDENTIAL
#: FIELD EXISTS IN THIS SHAPE — not optional, ABSENT — for the same structural
#: reason `ModelProviderBinding` has none: the dataclass is frozen and slotted,
#: so an extra keyword is a `TypeError` at construction and an extra attribute is
#: an `AttributeError` at assignment.
DECLARATION_FIELDS: tuple[str, ...] = (
    "binding_id",
    "status",
    "install_posture",
    "proposed_by",
    "proposed_at",
    "issued_by",
    "approved_by",
    "expires_at",
    "audit_ref",
    "consent_ref",
)

#: The fields a PENDING declaration may not carry. A pending record that already
#: named an approver would be an approval nobody performed.
_APPROVAL_ONLY_FIELDS: tuple[str, ...] = (
    "issued_by", "approved_by", "expires_at", "audit_ref")

#: Where a checkout's declarations live when nothing said otherwise: beside the
#: bindings, under the served checkout. A declaration is safe to commit — it
#: names a binding, an approver and an audit reference, and holds no secret — and
#: an operator reading their repository should be able to see which models their
#: install has approved and which are still waiting on a human.
DEFAULT_DECLARATIONS_RELPATH = "ideation/dashboard/model-declarations.yaml"

#: How long an approval is good for. A POLICY CONSTANT, not an operator input:
#: `credential-contracts` holds that a grant without `expires_at` is invalid, and
#: an expiry a requester chooses is an expiry that is always far away. Ninety
#: days is the same order as the rotation windows the credential family's own
#: binding templates carry.
APPROVAL_LIFETIME_DAYS = 90


class IntakeRefused(ValueError):
    """A declaration, a broker block, a store document, or an approval is not
    well-formed. ONE exception class for every refusal this module raises, so a
    caller running an intake has exactly one thing to catch."""


def _require_non_blank_str(field: str, value: object) -> str:
    if not isinstance(value, str):
        raise IntakeRefused(
            f"{field} must be a str, got {type(value).__name__}")
    if not value.strip():
        raise IntakeRefused(f"{field} must not be blank")
    return value


# ---------------------------------------------------------------------------
# the fixed sentences (composed from nothing an operator or a broker supplied)
# ---------------------------------------------------------------------------

#: What the flow says when this install declares no credential broker. THE FLOW
#: REFUSES RATHER THAN DEGRADING, and this is the reason it states: a wizard that
#: collected a key with nowhere governed to put it would have to hold it
#: somewhere, and every somewhere available to the dashboard is a place this
#: workspace's standing rule forbids.
NO_BROKER_NOTICE = (
    "no credential broker is declared on this install, so there is nowhere "
    "governed to put a provider credential; this flow presents no field that "
    "would accept one. Declare a broker first — the dashboard cannot invent "
    "one, and a credential it held itself would violate the rule this flow "
    "exists to keep")

#: What a completed intake says about custody. A MODULE CONSTANT, composed from
#: nothing an operator supplied, so every surface that discloses an intake says
#: the same thing.
CUSTODY_NOTICE = binding_mod.CUSTODY_NOTICE

#: What a completed intake says about availability. The whole point of the
#: pending state, in the words a human reads at the moment they might otherwise
#: assume they are finished.
PENDING_NOTICE = (
    "this model is DECLARED and not yet approved: it contributes no available "
    "catalog entry and no turn can name it. Approval is a separate recorded act "
    "by the human at this console")

#: What the OAUTH kind says on an install whose declared broker refuses one.
#: HONEST AND NOT A SIMULATION: the dashboard never becomes the party that
#: receives a provider's tokens, so when the broker declines to open its own
#: authorization flow the answer is that no authorization flow exists to hand the
#: human to — never a redirect this dashboard invented, and never a field of its
#: own that would take token material.
OAUTH_UNAVAILABLE_NOTICE = (
    "the declared credential broker did not open an authorization flow for a "
    "delegated subscription, so there is nowhere to hand you. This dashboard "
    "never receives a provider token of any kind and will not stand in for a "
    "broker that has not declared the flow: enrol a key the broker takes "
    "custody of, or declare a broker whose own surface performs the "
    "authorization")

#: What an approval says it did NOT do. Stated rather than implied, because an
#: operator who believes approving a model also bought them something is worse
#: off than one who knows it did not.
APPROVAL_NOTICE = (
    "the model is approved for this console and becomes an available catalog "
    "entry; the credential remains in the broker's custody and this act neither "
    "mints nor reads one")


def auth_kind_disclosure() -> list[dict]:
    """The authentication kinds this flow offers, as a surface may disclose them.

    READ FROM `doxbench_binding.AUTH_KINDS`, never respelled, so the flow and the
    record it writes cannot drift into two vocabularies. `accepts_secret` is the
    fact a renderer actually needs: it is what decides whether a field that would
    take a credential is presented at all, and it is stated here — on the server,
    beside the vocabulary — rather than inferred in a browser from the kind's
    name.

    THE BROWSER NEVER SPELLS THESE VALUES. It renders the label, submits the
    `kind` verbatim, and compares nothing: the workspace's absolute views clause
    keeps every credential-shaped spelling out of every page, so a page that
    hard-coded the kind would be carrying exactly the vocabulary that clause
    forbids."""
    return [
        {
            "kind": binding_mod.AUTH_KIND_API_KEY,
            "label": "a key I hold from the provider",
            "accepts_secret": True,
            "note": "the value goes straight to the broker and never becomes a "
                    "value this dashboard holds, writes, echoes or logs",
        },
        {
            "kind": binding_mod.AUTH_KIND_OAUTH,
            "label": "a subscription I authorize at the provider",
            "accepts_secret": False,
            "note": "the broker's own surface performs the authorization; this "
                    "dashboard is handed a reference and never a token of any "
                    "kind",
        },
    ]


# ---------------------------------------------------------------------------
# the broker declaration
# ---------------------------------------------------------------------------


@dataclasses.dataclass(frozen=True, slots=True)
class BrokerDeclaration:
    """WHERE THE BROKER IS, and nothing else.

    ONE field, and the absence of a second is the point: this record names the
    program and its fixed leading arguments — the part only the operator can
    know — and names no operation, no flag and no credential. The SUBCOMMANDS
    and FLAGS are the broker's own declaration and are recorded in
    `doxbench_provider`, read from `docs/broker-cli.md`, so four argv templates
    in a settings file cannot become four ways to get the declaration subtly
    wrong.

    argv, NEVER a shell string, for the same reason `broker_argv` is on a
    binding: no operator's label and no credential reference may ever be read as
    shell syntax."""

    argv: tuple[str, ...]

    def __post_init__(self) -> None:
        if isinstance(self.argv, (str, bytes)):
            raise IntakeRefused(
                "the broker declaration's argv must be a sequence of argv "
                f"members, not a single {type(self.argv).__name__} — a shell "
                "string would let a declared value be read as shell syntax")
        try:
            argv = tuple(str(member) for member in self.argv)
        except TypeError as error:
            raise IntakeRefused(
                "the broker declaration's argv must be an iterable of argv "
                f"members, got {type(self.argv).__name__}") from error
        object.__setattr__(self, "argv", argv)
        if not argv:
            raise IntakeRefused(
                "the broker declaration must name the broker command; an empty "
                "invocation is a broker that can never take custody")
        for member in argv:
            _require_non_blank_str("broker argv member", member)

    def as_record(self) -> dict:
        return {"kind": BROKER_KIND, "argv": list(self.argv)}

    @classmethod
    def from_record(cls, record: object) -> "BrokerDeclaration":
        if not isinstance(record, Mapping):
            raise IntakeRefused(
                "a broker declaration must be a mapping, got "
                f"{type(record).__name__}")
        unknown = sorted(set(record) - {"kind", "argv"})
        if unknown:
            raise IntakeRefused(
                f"a broker declaration declares unknown keys {unknown}; this "
                "shape holds exactly ['argv'] and no credential field exists "
                "in it")
        declared_kind = record.get("kind", BROKER_KIND)
        if declared_kind != BROKER_KIND:
            raise IntakeRefused(
                f"a broker declaration declares kind {declared_kind!r}, not "
                f"{BROKER_KIND!r}")
        if "argv" not in record:
            raise IntakeRefused("a broker declaration is missing ['argv']")
        return cls(argv=record["argv"])


# ---------------------------------------------------------------------------
# the declaration
# ---------------------------------------------------------------------------


@dataclasses.dataclass(frozen=True, slots=True)
class ModelDeclaration:
    """ONE model this flow declared, and whether a human has approved it.

    THE PAIRING IS ENFORCED AT CONSTRUCTION, not by a caller's care. A `pending`
    record carries no approval field at all, and an `approved` record carries all
    four of them — because a half-filled approval is exactly the shape that lets
    a reader believe a model was answerable when it was not. `consent_ref` obeys
    Brett's OQ-3 ruling in the same structural way: REQUIRED on a shared install
    and REFUSED on a single-operator one, so the record cannot state that a
    consent instrument was taken on the install the ruling says does not need
    one."""

    binding_id: str
    status: str
    install_posture: str
    proposed_by: str
    proposed_at: str
    issued_by: str | None = None
    approved_by: str | None = None
    expires_at: str | None = None
    audit_ref: str | None = None
    consent_ref: str | None = None

    def __post_init__(self) -> None:
        for field in ("binding_id", "status", "install_posture", "proposed_by",
                      "proposed_at"):
            _require_non_blank_str(field, getattr(self, field))
        if self.status not in STATUSES:
            raise IntakeRefused(
                f"status {self.status!r} is outside the closed vocabulary "
                f"{STATUSES}")
        if self.install_posture not in POSTURES:
            raise IntakeRefused(
                f"install_posture {self.install_posture!r} is outside the "
                f"closed vocabulary {POSTURES}")
        present = [field for field in _APPROVAL_ONLY_FIELDS
                   if getattr(self, field) is not None]
        if self.status == STATUS_PENDING:
            if present:
                raise IntakeRefused(
                    f"a pending declaration carries no approval facts, but "
                    f"{sorted(present)} were given; a record that named an "
                    "approver nobody was would be an approval nobody performed")
            if self.consent_ref is not None:
                raise IntakeRefused(
                    "a pending declaration carries no consent reference; "
                    "consent is taken at the approval, not at the proposal")
            return
        missing = [field for field in _APPROVAL_ONLY_FIELDS
                   if getattr(self, field) is None]
        if missing:
            raise IntakeRefused(
                f"an approved declaration must carry {sorted(missing)}; "
                "`credential-contracts` holds that a grant without an issuer, "
                "an approver, an expiry and an audit reference is invalid")
        for field in _APPROVAL_ONLY_FIELDS:
            _require_non_blank_str(field, getattr(self, field))
        if self.install_posture == POSTURE_SHARED:
            if self.consent_ref is None:
                raise IntakeRefused(
                    "an approval on a shared or tenant install carries a "
                    "consent reference (Brett's OQ-3 ruling of 2026-08-21): a "
                    "model enrolled where a turn may process another party's "
                    "material needs a consent instrument, not only a recorded "
                    "gate action")
            _require_non_blank_str("consent_ref", self.consent_ref)
        elif self.consent_ref is not None:
            raise IntakeRefused(
                "an approval on a single-operator loopback console carries NO "
                "consent reference (Brett's OQ-3 ruling of 2026-08-21): the "
                "human is spending their own subscription on their own corpus, "
                "and a consent instrument recorded there would be ceremony "
                "without a second party")

    # -- projections --------------------------------------------------------

    def as_record(self) -> dict:
        """The STORED record: the record kind, then exactly the fields this
        declaration actually has, in `DECLARATION_FIELDS` order. An absent
        optional field is OMITTED rather than written as null, so a pending
        record and an approved one differ in what they say rather than in how
        much of it is empty."""
        record: dict = {"kind": DECLARATION_KIND}
        for field in DECLARATION_FIELDS:
            value = getattr(self, field)
            if value is not None:
                record[field] = value
        return record

    def as_read_back(self) -> dict:
        """The DISCLOSED declaration: the stored record, the fixed custody
        sentence, and — while it is pending — the sentence that says what pending
        MEANS. There is no credential material to redact here, which is the whole
        claim."""
        disclosed = self.as_record()
        disclosed["credential_custody"] = CUSTODY_NOTICE
        if self.status == STATUS_PENDING:
            disclosed["availability"] = PENDING_NOTICE
        return disclosed

    def approval_block(self) -> dict:
        """The `model_approval` block a gate-action record carries.

        Exactly `APPROVAL_FIELDS`, plus `consent_ref` where the ruling says one
        exists. Built HERE, from the declaration's own validated fields, so the
        record on disk and the declaration in the settings document cannot state
        two different approvals."""
        if self.status != STATUS_APPROVED:
            raise IntakeRefused(
                "a pending declaration has no approval to record; the gate "
                "action is what makes it approved, not the other way round")
        block = {field: getattr(self, field) for field in APPROVAL_FIELDS}
        if self.consent_ref is not None:
            block["consent_ref"] = self.consent_ref
        return block

    @classmethod
    def from_record(cls, record: object) -> "ModelDeclaration":
        """Build a declaration from a stored mapping, refusing an unknown key.

        Refusing rather than ignoring, for the reason `ModelProviderBinding`
        gives: a record carrying a key this shape does not know is a record
        written against a different contract, and silently dropping it would let
        a field an operator believed they had declared vanish without a word."""
        if not isinstance(record, Mapping):
            raise IntakeRefused(
                "a declaration record must be a mapping, got "
                f"{type(record).__name__}")
        permitted = {"kind", *DECLARATION_FIELDS}
        unknown = sorted(set(record) - permitted)
        if unknown:
            raise IntakeRefused(
                f"a declaration record declares unknown keys {unknown}; this "
                f"shape holds exactly {list(DECLARATION_FIELDS)} and no "
                "credential field exists in it")
        declared_kind = record.get("kind", DECLARATION_KIND)
        if declared_kind != DECLARATION_KIND:
            raise IntakeRefused(
                f"a declaration record declares kind {declared_kind!r}, not "
                f"{DECLARATION_KIND!r}")
        required = ("binding_id", "status", "install_posture", "proposed_by",
                    "proposed_at")
        missing = [field for field in required if field not in record]
        if missing:
            raise IntakeRefused(f"a declaration record is missing {missing}")
        return cls(**{field: record.get(field)
                      for field in DECLARATION_FIELDS})


def approval_expiry(now: datetime | None = None) -> str:
    """When an approval taken NOW stops being good, as an RFC 3339 stamp.

    Derived from one policy constant rather than taken from a caller: an expiry
    the requester chooses is an expiry that is always far away."""
    moment = now if now is not None else datetime.now(timezone.utc)
    return (moment + timedelta(days=APPROVAL_LIFETIME_DAYS)).strftime(
        "%Y-%m-%dT%H:%M:%SZ")


def stamp(now: datetime | None = None) -> str:
    """One RFC 3339 stamp, in the spelling every record in this family uses."""
    moment = now if now is not None else datetime.now(timezone.utc)
    return moment.strftime("%Y-%m-%dT%H:%M:%SZ")


# ---------------------------------------------------------------------------
# the store
# ---------------------------------------------------------------------------

#: What a store says when the interpreter running it has no YAML parser. A FIXED
#: sentence, because the caller that catches it is an entrypoint choosing a
#: posture and not a human debugging an import.
NO_YAML_NOTICE = (
    "this install has no YAML parser (PyYAML), so a declarations document "
    "cannot be read or written; the install serves its declared posture "
    "without one")


def _yaml_or_refused():
    """The YAML parser, or an `IntakeRefused` — never a `ModuleNotFoundError`.

    The same guard `doxbench_binding` keeps and for the same measured reason:
    both entrypoints resolve their model port through this family at startup, so
    a bare `ModuleNotFoundError` here would kill a hosted serve before it printed
    its URL instead of falling back to its harness declaration."""
    try:
        import yaml
    except ModuleNotFoundError as error:
        raise IntakeRefused(NO_YAML_NOTICE) from error
    return yaml


class DeclarationStore:
    """What this checkout has declared and what a human has approved.

    Read-through and write-through, exactly like `BindingStore`: every verb reads
    the document, acts, and writes it back, so two operator doors cannot hold
    divergent in-memory copies. There is no cache to go stale, and a store nobody
    has written yet reads as an empty list rather than as an error — an install
    that has declared nothing is a posture, not a fault.
    """

    def __init__(self, path: Path | str) -> None:
        self.path = Path(path)

    # -- reading ------------------------------------------------------------

    def broker(self) -> BrokerDeclaration | None:
        """The declared broker, or None. None is the posture the intake flow
        REFUSES on — see `NO_BROKER_NOTICE` — never a reason to degrade."""
        return self._load()[0]

    def list(self) -> tuple[ModelDeclaration, ...]:
        """Every declaration, in declaration order."""
        return tuple(self._load()[1])

    def get(self, binding_id: str) -> ModelDeclaration | None:
        """One declaration by the binding it names, or None. Exact match; no
        case folding."""
        for declaration in self._load()[1]:
            if declaration.binding_id == binding_id:
                return declaration
        return None

    def pending_binding_ids(self) -> frozenset[str]:
        """The bindings this document says are DECLARED BUT NOT APPROVED.

        The one question the port factory asks. A binding this document says
        nothing about is absent from this set, which is what keeps a
        hand-declared install's posture byte-identical (see the module
        docstring)."""
        return frozenset(
            declaration.binding_id for declaration in self._load()[1]
            if declaration.status == STATUS_PENDING)

    def read_back(self) -> dict:
        """The whole store as a DISCLOSURE: the document's own identity, the
        broker's argv, and every declaration's read-back. Safe to print, safe to
        log, safe to paste into a review — there is no credential material in any
        of it."""
        broker, declarations = self._load()
        return {
            "schema_version": SCHEMA_VERSION,
            "kind": DECLARATIONS_KIND,
            "broker": broker.as_record() if broker is not None else None,
            "declarations": [d.as_read_back() for d in declarations],
        }

    # -- writing ------------------------------------------------------------

    def declare_broker(self, broker: BrokerDeclaration) -> BrokerDeclaration:
        """Name the program that will hold this install's credentials. Replaces
        any previous declaration: an install talks to one broker, and two would
        be two custodies for one console."""
        _broker, declarations = self._load()
        self._save(broker, declarations)
        return broker

    def propose(self, declaration: ModelDeclaration) -> ModelDeclaration:
        """Record a PENDING declaration. A repeated binding id refuses rather
        than replacing: a declaration already approved must not be silently
        reverted to pending by a second intake, and one already pending is
        already the state the caller wanted."""
        if declaration.status != STATUS_PENDING:
            raise IntakeRefused(
                "an intake proposes; it does not approve. A declaration "
                "entering this store carries the pending status, and the "
                "recorded human act is what changes it")
        broker, declarations = self._load()
        current = list(declarations)
        if any(existing.binding_id == declaration.binding_id
               for existing in current):
            raise IntakeRefused(
                f"a declaration for the binding {declaration.binding_id!r} "
                "already exists in this document")
        current.append(declaration)
        self._save(broker, current)
        return declaration

    def approve(self, binding_id: str, *, issued_by: str, approved_by: str,
                expires_at: str, audit_ref: str,
                consent_ref: str | None = None) -> ModelDeclaration:
        """Turn a pending declaration into an approved one.

        THE RECORD COMES FIRST. This method only writes the settings document;
        the gate-action record naming the declaration is written by the caller
        BEFORE it is called, so a crash between the two leaves an audit record
        for an approval that did not take effect — which is recoverable and
        readable — rather than an available model no record accounts for."""
        broker, declarations = self._load()
        current = list(declarations)
        for index, existing in enumerate(current):
            if existing.binding_id != binding_id:
                continue
            if existing.status == STATUS_APPROVED:
                raise IntakeRefused(
                    f"the binding {binding_id!r} is already approved; a second "
                    "approval would record an act with no effect")
            approved = dataclasses.replace(
                existing, status=STATUS_APPROVED, issued_by=issued_by,
                approved_by=approved_by, expires_at=expires_at,
                audit_ref=audit_ref, consent_ref=consent_ref)
            current[index] = approved
            self._save(broker, current)
            return approved
        raise IntakeRefused(
            f"no declaration for the binding {binding_id!r} is pending in this "
            "document; there is nothing here to approve")

    # -- the document -------------------------------------------------------

    def _load(self) -> tuple[BrokerDeclaration | None, list[ModelDeclaration]]:
        if not self.path.is_file():
            # THE HOSTED PATH, and the reason the import below is lazy: an
            # install with no declarations answers here and never needs a YAML
            # parser at all.
            return None, []
        yaml = _yaml_or_refused()
        try:
            document = yaml.safe_load(self.path.read_text(encoding="utf-8"))
        except yaml.YAMLError as error:
            raise IntakeRefused(
                f"the declarations document at {self.path} is not readable "
                "YAML") from error
        if document is None:
            return None, []
        if not isinstance(document, Mapping):
            raise IntakeRefused(
                f"the declarations document at {self.path} is not a mapping")
        if document.get("kind") != DECLARATIONS_KIND:
            raise IntakeRefused(
                f"the declarations document at {self.path} declares kind "
                f"{document.get('kind')!r}, not {DECLARATIONS_KIND!r}")
        if document.get("schema_version") != SCHEMA_VERSION:
            raise IntakeRefused(
                f"the declarations document at {self.path} declares "
                f"schema_version {document.get('schema_version')!r}, not "
                f"{SCHEMA_VERSION}")
        raw_broker = document.get("broker")
        broker = (BrokerDeclaration.from_record(raw_broker)
                  if raw_broker is not None else None)
        records = document.get("declarations") or []
        if not isinstance(records, list):
            raise IntakeRefused(
                f"the declarations document at {self.path} declares a non-list "
                "declarations key")
        declarations = [ModelDeclaration.from_record(record)
                        for record in records]
        seen: set[str] = set()
        for declaration in declarations:
            if declaration.binding_id in seen:
                raise IntakeRefused(
                    f"the declarations document at {self.path} declares the "
                    f"binding {declaration.binding_id!r} twice")
            seen.add(declaration.binding_id)
        return broker, declarations

    def _save(self, broker: BrokerDeclaration | None,
              declarations: Iterable[ModelDeclaration]) -> None:
        yaml = _yaml_or_refused()
        document = {
            "schema_version": SCHEMA_VERSION,
            "kind": DECLARATIONS_KIND,
            "broker": broker.as_record() if broker is not None else None,
            "declarations": [d.as_record() for d in declarations],
        }
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(
            yaml.safe_dump(document, sort_keys=False, allow_unicode=True),
            encoding="utf-8")


def declarations_path(checkout_root: Path | str) -> Path:
    """The default store path for a checkout. ONE rule, so two entrypoints
    cannot drift into reading two different files."""
    return Path(checkout_root) / DEFAULT_DECLARATIONS_RELPATH


def pending_binding_ids(checkout_root: Path | str,
                        declarations_file: Path | str | None = None
                        ) -> frozenset[str]:
    """The pending set for a checkout, or an EMPTY set when the document cannot
    be read.

    Empty on failure is the safe direction HERE and it is worth saying why, since
    fail-open is usually the wrong instinct: this set SUPPRESSES bindings, so an
    unreadable document that suppressed everything would take an operator's
    working console down over a settings-file typo — the same failure
    `declared_model_port_factory` already refuses to take. A document that cannot
    be read has declared nothing pending, and the operator's hand-declared
    bindings behave exactly as they did before this change."""
    store = DeclarationStore(
        declarations_file if declarations_file is not None
        else declarations_path(checkout_root))
    try:
        return store.pending_binding_ids()
    except IntakeRefused:
        return frozenset()
