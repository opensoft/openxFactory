"""`xfc-jcs-sha256-1` — the ONE digest construction in force for the
`signed-execution-chain` family.

The construction is declared in the contract
(`contracts/signed-execution-chain/digest-construction.schema.yaml`); this module
is the running code that computes it, and it deliberately declares nothing the
contract does not.

  1. SERIALIZATION — RFC 8785 JSON Canonicalization Scheme: object members sorted
     by the UTF-16 code-unit order of their names, no insignificant whitespace,
     JSON string escaping restricted to the shortest legal form, output UTF-8.
  2. ADMITTED VALUE CLASSES — object, array, string, INTEGER, boolean, null. A
     non-integer number RAISES rather than being serialized.
  3. ALGORITHM AND ENCODING — SHA-256, rendered `sha256:` + 64 lowercase hex.

WHY THE NUMBER CLASS IS BOUNDED RATHER THAN IMPLEMENTED. RFC 8785 serializes
numbers by ECMAScript's `Number::toString`, which is the one part of JCS a second
implementation reliably gets wrong — and a digest two readers compute differently
is worse than a digest one of them refuses. No shape in this family declares a
non-integer number, so refusing what the family does not use costs nothing and
closes the disagreement. `bool` is checked BEFORE `int` because `True` is an
`int` in Python and would otherwise serialize as `1`.

AND THE BOUND APPLIES TO INTEGERS TOO, which the first version of this module
missed. `str(value)` is NOT ECMAScript number serialization once a value leaves
the exactly-representable range: an ECMAScript reader holds every number as a
double, so `9007199254740993` becomes `9007199254740992` there and stays itself
here, and above about 1e21 the two disagree on exponent form as well. Python's
integers are unbounded and the schemas set no ceiling, so two conforming readers
could derive different chain identities from the same record — silently, since
neither would report anything. Integers outside ±(2**53 - 1) are therefore
REFUSED, on exactly the reasoning that refuses non-integer numbers. Found by
Codex as a P2; the fix is the same bound one class wider, not a second rule.
Every integer this family actually declares — `schema_version`, `leaf_index`,
`tree_size`, `registry_version`, `record_version` — is small by orders of
magnitude.

WHY UTF-16 CODE UNITS AND NOT CODE POINTS. RFC 8785 sorts by UTF-16 code units,
which differs from code-point order for names carrying characters above the BMP
(a surrogate pair's leading unit sorts below U+E000-U+FFFF). Encoding each name
to UTF-16 big-endian and comparing the resulting bytes reproduces that order
exactly; sorting the Python string directly does not, and the difference is
invisible on every name this family happens to use today — which is what makes it
worth getting right now rather than on the day a name changes.
"""

from __future__ import annotations

import hashlib
from typing import Any

CONSTRUCTION = "xfc-jcs-sha256-1"
ALGORITHM = "sha256"
TAG = f"{ALGORITHM}:"

#: 2**53 - 1 — the largest integer an IEEE-754 double holds exactly, and
#: therefore the largest one an RFC 8785 reader and this one are guaranteed to
#: serialize identically. Beyond it the two disagree silently, which is the only
#: kind of disagreement a digest construction cannot survive.
MAX_EXACT_INTEGER = 2 ** 53 - 1

# The subjects this capability computes digests over. The enumeration is the
# contract's; it is repeated here as a frozen set the validator checks against so
# a subject the contract does not declare cannot reach a comparison.
SUBJECTS = frozenset({
    "ratified_subject",
    "signed_ratification",
    "transparency_log_leaf",
    "traveling_contract",
    "gate_verdict",
})

_ESCAPES = {
    0x08: "\\b",
    0x09: "\\t",
    0x0A: "\\n",
    0x0C: "\\f",
    0x0D: "\\r",
    0x22: '\\"',
    0x5C: "\\\\",
}


class ConstructionError(ValueError):
    """A value the construction refuses to serialize.

    Raised rather than resolved: the whole point of one construction is that two
    readers agree, and a reader that guesses at a value class the construction
    does not admit has stopped agreeing with the one that refuses it.
    """


def _escape(text: str) -> str:
    out = ['"']
    for char in text:
        code = ord(char)
        escape = _ESCAPES.get(code)
        if escape is not None:
            out.append(escape)
        elif code < 0x20:
            out.append(f"\\u{code:04x}")
        else:
            out.append(char)
    out.append('"')
    return "".join(out)


def _key_order(name: str) -> bytes:
    return name.encode("utf-16-be", errors="surrogatepass")


def serialize(value: Any) -> str:
    """RFC 8785 canonical JSON, over the admitted value classes only."""
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int):
        if abs(value) > MAX_EXACT_INTEGER:
            raise ConstructionError(
                f"{CONSTRUCTION} admits integers within "
                f"±{MAX_EXACT_INTEGER} only; {value} is outside the range every "
                f"reader serializes identically, and RFC 8785 would render it "
                f"through an ECMAScript double where this one renders it exactly")
        return str(value)
    if isinstance(value, str):
        return _escape(value)
    if isinstance(value, (list, tuple)):
        return "[" + ",".join(serialize(item) for item in value) + "]"
    if isinstance(value, dict):
        # The member names are checked BEFORE the sort, not inside it: a
        # non-string name would otherwise surface as an AttributeError from the
        # sort key, which is an implementation detail leaking where a refusal
        # belongs.
        for name in value:
            if not isinstance(name, str):
                raise ConstructionError(
                    f"{CONSTRUCTION} admits only string member names; got "
                    f"{type(name).__name__}")
        members = [f"{_escape(name)}:{serialize(value[name])}"
                   for name in sorted(value, key=_key_order)]
        return "{" + ",".join(members) + "}"
    if isinstance(value, float):
        raise ConstructionError(
            f"{CONSTRUCTION} admits no non-integer number: {value!r}. The family "
            f"declares none, and ECMAScript number serialization is the one part "
            f"of RFC 8785 a second implementation reliably gets wrong")
    raise ConstructionError(
        f"{CONSTRUCTION} admits object, array, string, integer, boolean and null "
        f"only; got {type(value).__name__}")


def digest(value: Any) -> str:
    """The tagged digest of `value` under the one construction in force."""
    payload = serialize(value).encode("utf-8")
    return TAG + hashlib.sha256(payload).hexdigest()


def is_tagged(value: Any) -> bool:
    """A digest carried untagged cannot be migrated without silently changing
    meaning, so the tag is checked wherever a digest value is read."""
    if not isinstance(value, str) or not value.startswith(TAG):
        return False
    body = value[len(TAG):]
    return len(body) == 64 and all(char in "0123456789abcdef" for char in body)
