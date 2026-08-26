"""The MODEL-PROVIDER BINDING: what this dashboard holds instead of a secret
(add-model-provider-broker tasks 1.1/1.2).

A binding is the whole of what settings store for a model provider: an id, a
label, the credential REFERENCE the broker resolves, the authentication kind,
and the broker invocation. It is safe to read, safe to log and safe to commit,
which is precisely why it is the only thing kept here — the standing rule for
this workspace is that machinery holds grant and binding templates only, and
`credential-contracts` already owns the shape this applies
(`xfactory_credential_binding_template`: a consumer holds a binding and never a
secret).

NO SECRET FIELD EXISTS IN THIS SHAPE. Not optional, ABSENT. `ModelProviderBinding`
is a frozen, slotted dataclass, so there is no attribute a code path could
populate with a key or a token and no keyword a caller could pass to try: an
extra keyword is a `TypeError` at construction, and an extra attribute is an
`AttributeError` at assignment. That is the enforcement — not a convention, and
not a validator that a later edit could soften.

WHAT IS NOT IN THIS MODULE, deliberately: the broker itself, the credential
hand-off, the minted token, and every provider endpoint. All four live in
`doxbench_provider`, the ONE module this repository permits to hold them, and
the structural boundary test names that module by name. This one holds records
and a file, reaches no network, spawns no process, and never sees a credential.

THE ARGV TEMPLATE IS DECLARED, NOT WRITTEN INTO CODE. openProfiler — the broker
Brett's 2026-08-08 ruling names — is not built yet, so a command line this
repository cannot verify must not be frozen into it. The binding carries the
template; `doxbench_provider` substitutes and executes it. When openProfiler
ships with a different surface the binding changes and no code does.

STDLIB AT IMPORT TIME, and `yaml` only when a document is actually parsed or
written. That is not tidiness: the LEAN HOSTED IMAGE HAS NO PyYAML, and
`tests/ideation-dashboard/test_repo_selector.py`'s hosted-plane test proves it
by poisoning the module and serving anyway. Both entrypoints resolve their
model port through this store at startup, so a module-scope `import yaml` here
would have made every hosted serve die before it printed its URL — measured,
not theorised. A store with no document reads as empty without touching the
parser at all, so an install with no bindings never needs the dependency.
`doxbench_scope` takes the same lazy import for the same class of reason.
"""

from __future__ import annotations

import dataclasses
from collections.abc import Iterable, Mapping
from pathlib import Path

# ---------------------------------------------------------------------------
# the record's identity (the workspace rule: every YAML carries both)
# ---------------------------------------------------------------------------

#: The stored document's `schema_version`. The DOCUMENT's version governs every
#: record in it; a per-record version would be a second thing to keep in step.
SCHEMA_VERSION = 1

#: The stored document's `kind` — a list of bindings.
BINDINGS_KIND = "model-provider-bindings"

#: One record's own `kind`, stamped on each entry so a binding lifted out of the
#: document still says what it is. This is the `model-provider-binding` record
#: task 1.1 names.
BINDING_KIND = "model-provider-binding"

# ---------------------------------------------------------------------------
# the closed vocabularies
# ---------------------------------------------------------------------------

#: A long-lived API key the broker takes custody of.
AUTH_KIND_API_KEY = "api_key"

#: An OAuth grant the broker holds and refreshes.
AUTH_KIND_OAUTH = "oauth"

#: The CLOSED authentication-kind vocabulary. Closed because a free-text kind
#: riding a record that neither declares nor forbids it is unenforceable and
#: invisible to every consumer — the same argument `credential-contracts` makes
#: for its own `issuance_preconditions` vocabulary.
AUTH_KINDS: tuple[str, ...] = (AUTH_KIND_API_KEY, AUTH_KIND_OAUTH)

#: The exact, ordered field list a binding declares. Nothing else may appear in
#: a stored record, and nothing else appears in a read-back.
BINDING_FIELDS: tuple[str, ...] = (
    "id",
    "label",
    "credential_ref",
    "auth_kind",
    "broker_argv",
)

#: The CLOSED placeholder vocabulary an argv template may name. Every member is
#: a field of the binding itself, which is the property that matters: a template
#: can only ever be filled with facts the binding already discloses, so no
#: substitution can smuggle a value the record does not carry. A template naming
#: anything outside this set is refused at construction rather than at
#: execution — an operator finds out when they declare the binding, not when a
#: turn fails.
ARGV_PLACEHOLDERS: tuple[str, ...] = ("binding_id", "credential_ref", "auth_kind")

#: The fixed sentence a read-back states about custody (task 1.2: "read-back
#: discloses the binding and states plainly that the credential lives in the
#: broker"). A MODULE CONSTANT, composed from nothing an operator supplied, so
#: every surface that discloses a binding says the same thing.
CUSTODY_NOTICE = (
    "the credential itself is held by the broker this binding names; this "
    "dashboard stores only the reference above and can disclose nothing more")

#: Where a checkout's bindings live when nothing said otherwise. Beside the gate
#: records, under the served checkout, because a binding IS safe to commit and
#: an operator reading their repository should be able to see what their install
#: is bound to. Never a home directory and never a hidden state dir: an install
#: whose model provider is invisible to its own repository is the posture this
#: record exists to end.
DEFAULT_BINDINGS_RELPATH = "ideation/dashboard/model-provider-bindings.yaml"


class BindingRefused(ValueError):
    """A binding, a store document, or an argv substitution is not
    well-formed. ONE exception class for every refusal this module raises, so a
    caller declaring a binding has exactly one thing to catch."""


def _require_non_blank_str(field: str, value: object) -> str:
    if not isinstance(value, str):
        raise BindingRefused(
            f"{field} must be a str, got {type(value).__name__}")
    if not value.strip():
        raise BindingRefused(f"{field} must not be blank")
    return value


@dataclasses.dataclass(frozen=True, slots=True)
class ModelProviderBinding:
    """ONE model provider, as settings hold it.

    Five fields, and the absence of a sixth is the point (see the module
    docstring). `broker_argv` is the DECLARED invocation as a tuple of argv
    members — argv, never a shell string, so no operator's label and no
    credential reference can ever be read as shell syntax.
    """

    id: str
    label: str
    credential_ref: str
    auth_kind: str
    broker_argv: tuple[str, ...]

    def __post_init__(self) -> None:
        for field in ("id", "label", "credential_ref", "auth_kind"):
            _require_non_blank_str(field, getattr(self, field))
        if self.auth_kind not in AUTH_KINDS:
            raise BindingRefused(
                f"auth_kind {self.auth_kind!r} is outside the closed "
                f"vocabulary {AUTH_KINDS}")
        if isinstance(self.broker_argv, (str, bytes)):
            raise BindingRefused(
                "broker_argv must be a sequence of argv members, not a single "
                f"{type(self.broker_argv).__name__} — a shell string would let "
                "a declared value be read as shell syntax")
        try:
            argv = tuple(str(member) for member in self.broker_argv)
        except TypeError as error:
            raise BindingRefused(
                "broker_argv must be an iterable of argv members, got "
                f"{type(self.broker_argv).__name__}") from error
        object.__setattr__(self, "broker_argv", argv)
        if not argv:
            raise BindingRefused(
                "broker_argv must name the broker command; an empty invocation "
                "is a binding that can never mint")
        for member in argv:
            _require_non_blank_str("broker_argv member", member)
            for name in _placeholder_names(member):
                if name not in ARGV_PLACEHOLDERS:
                    raise BindingRefused(
                        f"broker_argv names the placeholder {{{name}}}, which "
                        f"is outside the closed vocabulary {ARGV_PLACEHOLDERS}")

    # -- projections --------------------------------------------------------

    def as_record(self) -> dict:
        """The STORED record: the record kind, then exactly ``BINDING_FIELDS``
        in order. `broker_argv` becomes a list because that is what YAML round
        trips; nothing else changes shape."""
        return {
            "kind": BINDING_KIND,
            "id": self.id,
            "label": self.label,
            "credential_ref": self.credential_ref,
            "auth_kind": self.auth_kind,
            "broker_argv": list(self.broker_argv),
        }

    def as_read_back(self) -> dict:
        """The DISCLOSED binding (task 1.2): the stored record plus the fixed
        custody sentence, and nothing else.

        There is no credential material to redact here, which is the whole
        claim: a read-back cannot leak a secret it was never able to hold. The
        sentence says so in words rather than leaving the absence to be
        inferred from a missing key."""
        disclosed = self.as_record()
        disclosed["credential_custody"] = CUSTODY_NOTICE
        return disclosed

    def substituted_argv(self) -> tuple[str, ...]:
        """The declared invocation with its placeholders filled from this
        binding's own fields.

        PURE, and it is here rather than in the executing module on purpose:
        substitution is a fact about the record, so it can be asserted without
        spawning anything. `doxbench_provider` calls this and then executes the
        result; it never builds an argv of its own."""
        values = {
            "binding_id": self.id,
            "credential_ref": self.credential_ref,
            "auth_kind": self.auth_kind,
        }
        return tuple(_substitute(member, values) for member in self.broker_argv)

    @classmethod
    def from_record(cls, record: object) -> "ModelProviderBinding":
        """Build a binding from a stored mapping, refusing an unknown key.

        Refusing rather than ignoring: a record carrying a key this shape does
        not know is a record written against a different contract, and silently
        dropping it would let a field an operator believed they had declared
        (a secret, most dangerously) vanish without a word."""
        if not isinstance(record, Mapping):
            raise BindingRefused(
                f"a binding record must be a mapping, got "
                f"{type(record).__name__}")
        permitted = {"kind", *BINDING_FIELDS}
        unknown = sorted(set(record) - permitted)
        if unknown:
            raise BindingRefused(
                f"a binding record declares unknown keys {unknown}; this shape "
                f"holds exactly {list(BINDING_FIELDS)} and no credential field "
                "exists in it")
        declared_kind = record.get("kind", BINDING_KIND)
        if declared_kind != BINDING_KIND:
            raise BindingRefused(
                f"a binding record declares kind {declared_kind!r}, not "
                f"{BINDING_KIND!r}")
        missing = [field for field in BINDING_FIELDS if field not in record]
        if missing:
            raise BindingRefused(
                f"a binding record is missing {missing}")
        return cls(
            id=record["id"],
            label=record["label"],
            credential_ref=record["credential_ref"],
            auth_kind=record["auth_kind"],
            broker_argv=record["broker_argv"],
        )


def _placeholder_names(member: str) -> tuple[str, ...]:
    """Every `{name}` in one argv member, without importing a formatter.

    Hand-scanned rather than delegated to `string.Formatter` because the doubled
    braces `{{`/`}}` a formatter treats as escapes have no meaning in an argv
    member an operator wrote: `{{x}}` there is a literal the broker would
    receive with braces on it, and reading it as an escaped `{x}` would silently
    accept a template this vocabulary refuses."""
    names: list[str] = []
    rest = member
    while True:
        opened = rest.find("{")
        if opened < 0:
            return tuple(names)
        closed = rest.find("}", opened + 1)
        if closed < 0:
            raise BindingRefused(
                f"broker_argv member {member!r} opens a placeholder it never "
                "closes")
        names.append(rest[opened + 1:closed])
        rest = rest[closed + 1:]


def _substitute(member: str, values: Mapping[str, str]) -> str:
    out = member
    for name in ARGV_PLACEHOLDERS:
        out = out.replace("{" + name + "}", values[name])
    return out


# ---------------------------------------------------------------------------
# the store (task 1.2: list, add, edit, remove)
# ---------------------------------------------------------------------------


class BindingStore:
    """The bindings a checkout declares, as a file of records.

    Read-through and write-through: every verb reads the document, acts, and
    writes it back, so two operator doors (a CLI verb here, a future surface
    there) cannot hold divergent in-memory copies. There is no cache to go
    stale, and a store nobody has written yet reads as an empty list rather
    than as an error — an install with no model provider is a posture, not a
    fault.
    """

    def __init__(self, path: Path | str) -> None:
        self.path = Path(path)

    # -- reading ------------------------------------------------------------

    def list(self) -> tuple[ModelProviderBinding, ...]:
        """Every declared binding, in declaration order."""
        return tuple(self._load())

    def get(self, binding_id: str) -> ModelProviderBinding | None:
        """One binding by id, or None. Exact match; no case folding."""
        for binding in self._load():
            if binding.id == binding_id:
                return binding
        return None

    def read_back(self) -> dict:
        """The whole store as a DISCLOSURE (task 1.2): the document's own
        identity, every binding's read-back, and the fixed custody sentence on
        each. Safe to print, safe to log, safe to paste into a review."""
        return {
            "schema_version": SCHEMA_VERSION,
            "kind": BINDINGS_KIND,
            "bindings": [binding.as_read_back() for binding in self._load()],
        }

    # -- writing ------------------------------------------------------------

    def add(self, binding: ModelProviderBinding) -> ModelProviderBinding:
        """Declare a NEW binding. A repeated id refuses rather than replacing:
        an operator who meant to change one has `edit`, and a silent overwrite
        would retire a declaration nobody asked to retire."""
        current = list(self._load())
        if any(existing.id == binding.id for existing in current):
            raise BindingRefused(
                f"a binding with id {binding.id!r} is already declared; use "
                "edit to change it")
        current.append(binding)
        self._save(current)
        return binding

    def edit(self, binding: ModelProviderBinding) -> ModelProviderBinding:
        """Replace an EXISTING binding, in place, keeping its position. An
        unknown id refuses rather than adding: `add` is the verb for that, and
        an edit that quietly creates hides a mistyped id."""
        current = list(self._load())
        for index, existing in enumerate(current):
            if existing.id == binding.id:
                current[index] = binding
                self._save(current)
                return binding
        raise BindingRefused(
            f"no binding with id {binding.id!r} is declared; use add to "
            "declare one")

    def remove(self, binding_id: str) -> ModelProviderBinding:
        """Retire a binding. Returns the record that was removed, so a caller
        can report exactly what it retired.

        REMOVING A BINDING REMOVES NO CREDENTIAL. The credential lives in the
        broker; forgetting the reference here leaves it exactly where it was.
        That is stated by `REMOVAL_NOTICE` rather than implied, because an
        operator who believes a removal revoked something is worse off than one
        who knows it did not."""
        current = list(self._load())
        for index, existing in enumerate(current):
            if existing.id == binding_id:
                del current[index]
                self._save(current)
                return existing
        raise BindingRefused(f"no binding with id {binding_id!r} is declared")

    # -- the document ------------------------------------------------------

    def _load(self) -> list[ModelProviderBinding]:
        if not self.path.is_file():
            # THE HOSTED PATH, and the reason the import below is lazy: an
            # install with no bindings document answers here and never needs a
            # YAML parser at all.
            return []
        import yaml
        try:
            document = yaml.safe_load(self.path.read_text(encoding="utf-8"))
        except yaml.YAMLError as error:
            raise BindingRefused(
                f"the bindings document at {self.path} is not readable YAML"
            ) from error
        if document is None:
            return []
        if not isinstance(document, Mapping):
            raise BindingRefused(
                f"the bindings document at {self.path} is not a mapping")
        if document.get("kind") != BINDINGS_KIND:
            raise BindingRefused(
                f"the bindings document at {self.path} declares kind "
                f"{document.get('kind')!r}, not {BINDINGS_KIND!r}")
        if document.get("schema_version") != SCHEMA_VERSION:
            raise BindingRefused(
                f"the bindings document at {self.path} declares "
                f"schema_version {document.get('schema_version')!r}, not "
                f"{SCHEMA_VERSION}")
        records = document.get("bindings") or []
        if not isinstance(records, list):
            raise BindingRefused(
                f"the bindings document at {self.path} declares a non-list "
                "bindings key")
        bindings = [ModelProviderBinding.from_record(record)
                    for record in records]
        seen: set[str] = set()
        for binding in bindings:
            if binding.id in seen:
                raise BindingRefused(
                    f"the bindings document at {self.path} declares the id "
                    f"{binding.id!r} twice")
            seen.add(binding.id)
        return bindings

    def _save(self, bindings: Iterable[ModelProviderBinding]) -> None:
        import yaml
        document = {
            "schema_version": SCHEMA_VERSION,
            "kind": BINDINGS_KIND,
            "bindings": [binding.as_record() for binding in bindings],
        }
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(
            yaml.safe_dump(document, sort_keys=False, allow_unicode=True),
            encoding="utf-8")


#: What a removal does and does not do, stated once so no surface invents its
#: own weaker sentence.
REMOVAL_NOTICE = (
    "the binding is retired from this checkout; the credential it referenced "
    "remains in the broker's custody and is not revoked by this act")


def bindings_path(checkout_root: Path | str) -> Path:
    """The default store path for a checkout. ONE rule, so two entrypoints
    cannot drift into reading two different files."""
    return Path(checkout_root) / DEFAULT_BINDINGS_RELPATH
