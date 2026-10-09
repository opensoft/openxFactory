"""Provider reference implementation for the `council-convening` contract family.

Feature 035 (`specs/035-renew-resolved-council-protocol/`), realizing the ratified
change `renew-resolved-council-protocol`. The family's schemas, registries and
conformance corpus live under `contracts/council-convening/`; this package is the
third, independent implementation that adjudicates every corpus vector, beside
the producer's (codexFactory 049) and the consumer's (Hermes 025). It is written
from the family's own specification and imports nothing from either successor
(research R4).

ALWAYS IMPORT THIS PACKAGE AS `scripts.council_convening`. The test package is
`tests/council_convening/`, and pytest imports it under the bare name
`council_convening`; a bare import of this package would collide with it in
`sys.modules`. Modules inside the package import each other relatively.

Phase 1 delivers four modules, and later phases add one module each:

* `records`        — the schema registry, whole-match identifiers, the
                     canonicalizability pre-check and the `Refused` exception;
* `classification` — protocol classification and the selection-dependent
                     effects (data-model E1);
* `corpus`         — index closure, raw-byte digests, `$parts`, the boundary
                     dispatch table, adjudication and coverage at the commit;
* `generate`       — the deterministic corpus generator and the labelled
                     fixture keys (R18).

Nothing here selects or activates a protocol, listens on a socket, or holds a
key. A fixture key is derived from a public phrase, used in memory, and never
written.
"""
