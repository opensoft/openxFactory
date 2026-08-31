"""Ed25519 signature VERIFICATION, and `did:key` public-half recovery.

WHY THIS EXISTS AT ALL, stated first because "do not write your own crypto" is
the right default and this is a deliberate exception with a bounded shape.

  * The gate's first check is that THE RATIFICATION'S SIGNATURE VERIFIES. A gate
    that cannot perform it does not have eight checks; it has seven and a claim.
    This capability's own doctrine is that a control which is described and does
    not run is the failure it exists to end, so an unverifiable signature is a
    refusal — never a pass — and the honest way to avoid a permanent refusal is
    to be able to verify.
  * The repository's dependency floor is `requirements/hermes-runtime-contracts.lock`,
    a hash-pinned lock carrying PyYAML, jsonschema, referencing, rfc3339-validator
    and pytest. It carries no cryptography library, and adding one to a
    hash-pinned lock to verify a governance signature is a larger and less
    reviewable change than sixty lines of arithmetic that a published test vector
    pins.

WHAT MAKES THE EXCEPTION SAFE, precisely:

  * VERIFICATION ONLY. This module generates no key, signs nothing, and holds no
    secret. There is no secret for a timing side channel to leak, which is what
    the usual warning is about; every input is public and every branch is over
    public data.
  * IT IS THE RFC's OWN REFERENCE ALGORITHM, not a variant. RFC 8032 section 5.1.7
    verification, with the group equation checked in extended coordinates, `S`
    range-checked against the group order (a non-canonical `S` is a malleable
    signature and is refused), and both points rejected when they do not decompress.
  * PLUS THE ONE CHECK THE RFC's PSEUDOCODE OMITS: SMALL-ORDER POINTS ARE
    REFUSED. With an identity public key the `[h]A` term vanishes and the
    equation stops depending on the message, so `R = identity, S = 0` verifies
    for anything — a forgery needing no private key, and every public half here
    arrives inside a record chosen by whoever assembled the chain. Found by Codex
    and Copilot in the same round, both P1, and reproduced against this module's
    own pre-fix code before the repair. See `_is_small_order`.
  * IT IS PINNED BY PUBLISHED KNOWN-ANSWER VECTORS. `tests/signed_execution_chain/
    test_ed25519_known_answers.py` runs RFC 8032 section 7.1's vectors and their
    mutations — flipped message byte, flipped signature byte, wrong public key,
    truncated inputs, out-of-range `S`, and every small-order point — so a
    regression that accepted anything is a red test rather than a silently
    permissive gate.

WHAT IT DOES NOT DO. `ecdsa-p256` and `ecdsa-secp256k1` appear in the shipped
signature-algorithm enumeration and are NOT implemented here. A chain presenting
one is UNEVALUABLE, which is a refusal — the family's fail-closed doctrine, and
the opposite of accepting a signature nobody checked.
"""

from __future__ import annotations

import hashlib

# Curve25519 field and Ed25519 group parameters (RFC 8032 section 5.1).
_P = 2 ** 255 - 19
_L = 2 ** 252 + 27742317777372353535851937790883648493
_D = -121665 * pow(121666, _P - 2, _P) % _P
_SQRT_M1 = pow(2, (_P - 1) // 4, _P)

_BASE58 = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
_BASE58_INDEX = {char: index for index, char in enumerate(_BASE58)}
# multicodec `ed25519-pub`, varint-encoded.
_ED25519_MULTICODEC = b"\xed\x01"

SIGNATURE_BYTES = 64
PUBLIC_KEY_BYTES = 32


class KeyRecoveryError(ValueError):
    """A public half that cannot be recovered from what a record carries.

    Raised rather than returned as `False`: "this key is unresolvable" and "this
    signature does not verify" are different events, and collapsing them would
    report an unevaluable chain as a failed one.
    """


def _recover_x(y: int, sign: int) -> int | None:
    if y >= _P:
        return None
    x2 = (y * y - 1) * pow(_D * y * y + 1, _P - 2, _P) % _P
    if x2 == 0:
        return None if sign else 0
    x = pow(x2, (_P + 3) // 8, _P)
    if (x * x - x2) % _P != 0:
        x = x * _SQRT_M1 % _P
    if (x * x - x2) % _P != 0:
        return None
    if (x & 1) != sign:
        x = _P - x
    return x


_G_Y = 4 * pow(5, _P - 2, _P) % _P
_G_X = _recover_x(_G_Y, 0)
_G = (_G_X, _G_Y, 1, _G_X * _G_Y % _P)

_Point = tuple[int, int, int, int]


def _add(point: _Point, other: _Point) -> _Point:
    a = (point[1] - point[0]) * (other[1] - other[0]) % _P
    b = (point[1] + point[0]) * (other[1] + other[0]) % _P
    c = 2 * point[3] * other[3] * _D % _P
    d = 2 * point[2] * other[2] % _P
    return ((b - a) * (d - c) % _P, (d + c) * (b + a) % _P,
            (d - c) * (d + c) % _P, (b - a) * (b + a) % _P)


def _mul(scalar: int, point: _Point) -> _Point:
    result: _Point = (0, 1, 1, 0)
    while scalar > 0:
        if scalar & 1:
            result = _add(result, point)
        point = _add(point, point)
        scalar >>= 1
    return result


def _equal(point: _Point, other: _Point) -> bool:
    if (point[0] * other[2] - other[0] * point[2]) % _P != 0:
        return False
    return (point[1] * other[2] - other[1] * point[2]) % _P == 0


def _decompress(encoded: bytes) -> _Point | None:
    if len(encoded) != PUBLIC_KEY_BYTES:
        return None
    value = int.from_bytes(encoded, "little")
    sign = value >> 255
    y = value & ((1 << 255) - 1)
    x = _recover_x(y, sign)
    if x is None:
        return None
    return (x, y, 1, x * y % _P)


_IDENTITY: _Point = (0, 1, 1, 0)


def _is_small_order(point: _Point) -> bool:
    """True when the point's order divides 8 — the identity and the fourteen
    other small-order points on this curve.

    WHY THIS CHECK EXISTS, and it is the one thing RFC 8032's verification
    pseudocode does not tell you to do. The group equation is
    `[S]B == R + [h]A`. If `A` is the IDENTITY the `[h]A` term vanishes, the
    equation stops depending on `h` — and therefore on the message — and
    `R = identity, S = 0` satisfies it for EVERY message. An attacker who can
    choose the public half needs no private key at all, and every public half in
    this family arrives inside a record: a `did:key` in a CARRIED wallet, chosen
    by whoever assembled the chain.

    MEASURED AGAINST THIS MODULE'S OWN PRE-FIX CODE, which is why the wording is
    not hedged: the identity key accepted `R = identity, S = 0` over every
    message tried, and two of the order-4 points accepted it over some. Found by
    Codex and Copilot in the same round, both rated P1, and both right.

    `[8]A == identity` is exactly "the order divides 8", so one multiplication by
    8 — three doublings — rejects the whole class rather than a hard-coded list
    of encodings that a non-canonical spelling could slip past.
    """
    return _equal(_mul(8, point), _IDENTITY)


def verify(public_key: bytes, message: bytes, signature: bytes) -> bool:
    """RFC 8032 section 5.1.7 verification, plus the small-order rejection its
    pseudocode omits. False on every failure, never an exception: a signature
    that does not verify is an ANSWER, and the caller distinguishes it from an
    unresolvable key by asking for the key separately."""
    if len(public_key) != PUBLIC_KEY_BYTES or len(signature) != SIGNATURE_BYTES:
        return False
    point_a = _decompress(public_key)
    if point_a is None:
        return False
    if _is_small_order(point_a):
        # The forgery vector above. Refused before the equation is evaluated, so
        # there is no path on which a small-order key reaches a comparison.
        return False
    encoded_r = signature[:32]
    point_r = _decompress(encoded_r)
    if point_r is None:
        return False
    if _is_small_order(point_r):
        # NOT the forgery vector — with `A` in the prime-order subgroup a
        # small-order `R` confers no advantage — but an honest signer produces one
        # only when the hash-derived nonce is `0 mod L`, at probability about
        # 2**-252. Refusing it costs no legitimate signature and removes the
        # remaining case in which a signature's acceptance depends on a
        # cofactored reading of the equation.
        return False
    scalar_s = int.from_bytes(signature[32:], "little")
    if scalar_s >= _L:
        # A non-canonical S is a malleable signature: the same message and key
        # would verify under more than one signature, which is not what "the
        # signature over this ratification" is allowed to mean.
        return False
    challenge = int.from_bytes(
        hashlib.sha512(encoded_r + public_key + message).digest(), "little") % _L
    return _equal(_mul(scalar_s, _G), _add(point_r, _mul(challenge, point_a)))


def base58btc_decode(text: str) -> bytes:
    """Bitcoin-alphabet base58, the encoding `did:key`'s `z` multibase prefix
    names. Leading `1`s are leading zero bytes, which a bare integer conversion
    silently drops."""
    value = 0
    for char in text:
        index = _BASE58_INDEX.get(char)
        if index is None:
            raise KeyRecoveryError(f"not base58btc: {char!r}")
        value = value * 58 + index
    body = value.to_bytes((value.bit_length() + 7) // 8, "big") if value else b""
    leading = len(text) - len(text.lstrip("1"))
    return b"\x00" * leading + body


def public_key_from_multibase(multibase: str) -> bytes:
    """`z` + base58btc(multicodec `ed25519-pub` || 32 raw bytes) -> the 32 bytes."""
    if not isinstance(multibase, str) or not multibase.startswith("z"):
        raise KeyRecoveryError(
            f"multibase {multibase!r} is not base58btc-encoded (`z` prefix)")
    decoded = base58btc_decode(multibase[1:])
    if not decoded.startswith(_ED25519_MULTICODEC):
        raise KeyRecoveryError(
            "multibase payload does not carry the `ed25519-pub` multicodec "
            "prefix; this capability verifies ed25519 and nothing else")
    body = decoded[len(_ED25519_MULTICODEC):]
    if len(body) != PUBLIC_KEY_BYTES:
        raise KeyRecoveryError(
            f"ed25519 public half is {len(body)} bytes, expected {PUBLIC_KEY_BYTES}")
    return body


def public_key_from_did(did: str) -> bytes:
    """`did:key:z...` -> the 32 raw bytes. The DID is REQUIRED on every wallet
    `key_reference` by the pinned record schema, where `public_key_multibase` is
    optional — so the DID is what a carried wallet can always be read from, and
    the multibase, where present, is cross-checked against it rather than trusted
    beside it."""
    if not isinstance(did, str) or not did.startswith("did:key:"):
        raise KeyRecoveryError(
            f"{did!r} is not a `did:key` DID; this capability recovers a public "
            f"half from `did:key` only")
    return public_key_from_multibase(did[len("did:key:"):])
