# Design: retire-doxbench-chat-turn-v1

Status: draft
Proposed: 2026-09-01

The removal itself is mechanical. Two things are not, and this note is about
them: **what answers an unrecognized `kind` after the deprecated family is
gone**, and **what happens to the seven refusal classes only the v1 negative
fixtures carry**.

## 1. The fallback posture

### What is there today

`scripts/ideation_dashboard/serve.py:3541-3558` reads the family off the
request's own `kind` and answers in the family the request arrived in. The `else`
arm is the fallback and it is explicit about being one:

```python
request_kind = (payload.get("kind")
                if isinstance(payload.get("kind"), str) else None)
if request_kind == DOXBENCH_CHAT_TURN_V2_KIND:
    failure_kind = DOXBENCH_CHAT_TURN_V2_FAILURE_KIND
    parse_body = self._parse_workbench_chat_turn_v2_body
else:
    request_kind = DOXBENCH_CHAT_TURN_KIND
    failure_kind = DOXBENCH_CHAT_TURN_FAILURE_KIND
    parse_body = self._parse_workbench_chat_turn_body
```

with the stated reason that *"an unrecognized kind is answered in the v1 failure
family: a request that never named a family it could be answered in gets the
posture it would have got before this release"*.

**That reason is a statement about a world with two families.** Delete v1 and it
names nothing: the `else` arm would select a parser and an envelope kind that no
longer exist, and the branch that reads as a graceful default becomes a server
fault. This is precisely why the ruling says *redesigned, not deleted*.

### The second layer, which is NOT redesigned

`_refuse_turn` (`:3277-3317`) already has a fallback of its own. With no
wire-valid `turn_id` — or if the built envelope fails its own self-validation —
it leaves the contract envelope and answers in `doxbench_error_body`'s fixed
pre-identity shape. Its docstring states the rule that makes it correct: the
console *"never sends a wire shape the released schema has not accepted, and it
never invents a turn identity to obtain one"*.

That layer stays exactly as it is. It is the right answer for a request with no
identity, and it is the reason the redesign below can require a `client_turn_id`
without having to invent one.

### What replaces the first layer

**Chosen: refuse in the SURVIVING family, with an explicit unknown-kind code.**

| the request | the answer |
| --- | --- |
| `kind` is the surviving request kind | unchanged — parsed and served as today |
| `kind` is anything else (including a removed v1 kind, or absent) **and** a wire-valid `client_turn_id` is present | `workbench-chat-turn-v2-failure`, `error: <unknown-kind code>`, self-validated against the released schema before it is sent |
| `kind` is anything else **and** no wire-valid `client_turn_id` | the existing pre-identity `doxbench_error_body` shape, unchanged |

**Three measurements make it legal on the contract as it stands, and they are
the whole argument:**

1. `$defs/failure_v2` requires `schema_version`, `kind`, `client_turn_id`,
   `error`, `message` — and constrains `error` by the PATTERN
   `^[a-z][a-z0-9_]{2,63}$`, not by an enum. There is no code vocabulary in the
   schema.
2. The delegated validator that judges a v2 failure is the SAME function that
   judges a v1 failure (`check_turn_failure`), on the released reason that *"a v2
   failure discloses exactly what a v1 failure does, so it is judged by exactly
   the same function"*. It checks the `limit`⟺`request_limit_exceeded` pairing
   and scans `message` for leaks. It applies no code vocabulary either.
3. The only CLOSED list is `serve.py`'s own `DOXBENCH_ERROR_CATALOG`, which maps
   code to status and to a fixed message and raises on an unregistered code. So
   the new code costs exactly one catalog entry — **and that entry is not
   optional**, because without it the refusal path raises instead of refusing.

**Rejected: refuse outside any envelope.** Answer every unrecognized kind in the
pre-identity shape, whatever identity the request supplied. Simpler; asserts
less; recorded here so the choice is visible rather than implied. Rejected on
three costs, none of them large alone and all of them paid to avoid registering
one code: it discards an identity the request DID supply; it returns a body
carrying no `kind`, on a rail whose client dispatches on `kind`; and it puts the
refusal outside the contract, where no packaged fixture can cover it and no
validator can judge it.

**Not considered a third option: keeping a v1 failure envelope alive purely as
the fallback.** That is the retirement failing to happen, wearing a smaller
coat — one `$def`, one `oneOf` ref and one builder still shipped, still
registered, still needing the deprecation record to stay in force.

### One consequence stated

After the removal, **a retired v1 kind and a kind that never existed are the
same fact about the wire**, and both take this path. The refusal does not — and
should not — tell a client that the kind it sent used to work: the surviving
contract has no vocabulary for "removed at a major", and inventing one to soften
a refusal would put migration guidance on the wire instead of in the changelog,
where a consumer upgrading across the major actually reads it.

## 2. The seven refusal classes

The memo priced four fixtures. There are **twelve**, and the eight it missed are
the negatives. They matter more than the positives, because a negative fixture is
a REFUSAL that is being tested and the surviving family does not test the same
ones:

| carried by v1 negatives alone | carried by v2 negatives |
| --- | --- |
| escaping path, hash mismatch, identity subject, over budget, unknown model, untyped proposal, duplicate turn pair | context-packet posture (six variants), reserved key path, unbound buffer, provider-retry token leakage |

The two sets are almost disjoint. Deleting the v1 negatives with the family
therefore deletes seven refusals from the packaged corpus — not because anyone
decided those refusals no longer matter, but because the fixtures that exercised
them happened to be written in the retired envelope.

**The rule this change takes: each of the seven is either re-expressed as a
`-v2` negative, or recorded as a stated coverage loss with the reason.** Silence
is not a third option. Where a class is genuinely unreachable in the surviving
family — if any is — saying so is a finding worth keeping, and it is cheap to
write.

## 3. Why this is its own packet

The memo recommended it and the shape confirms it. This is the only one of
#522's three entries that moves **schema bytes** (so the manifest digest moves
and the inventory rebuilds), a **packaged corpus**, a **committed byte-identity
baseline**, and a **server posture that is a design decision rather than a
deletion**. The sibling moves validator code and policy prose and touches no
schema. Folding them together would put a schema-digest cut and a four-line
branch deletion behind one review, and would hide the one genuinely
non-mechanical decision in this whole issue — § 1 above — inside a packet whose
other two entries have none.
