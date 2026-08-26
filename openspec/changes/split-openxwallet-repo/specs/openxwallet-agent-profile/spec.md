# openxwallet-agent-profile Specification

This delta is the corpus EXIT of `openxwallet-agent-profile`. Under R3 of `split-openxwallet-repo`
the new repository owns the wallet's own standard and `openxFactory` keeps the
seam, so the three agent-holder requirements below leave this corpus for
`opensoft/openXwallet` and are promoted there instead. The successor location is
recorded in three places that survive the archive: this delta's prose,
`contracts/openxwallet-pin.yaml` as the live machine-readable pointer, and
`contracts/README.md` plus the `contracts/CHANGELOG.md` entry for the cut.

The mechanism is `document-lifecycle`'s requirement *Ratified spec deltas reach
the promoted specification* (`openspec/specs/document-lifecycle/spec.md:520-598`):
"a requirement it REMOVED SHALL be absent", and "a requirement still present
after its ratified removal MUST be reported". The titles below are reproduced
CHARACTER-FOR-CHARACTER from the promoted spec, because
`scripts/doc_health/promotion_fidelity.py` keys on (capability, normalized
title) and one character of drift leaves the 2026-08-08 `ADDED` writer
authoritative and this removal invisible to the checker.

No `superseded` header is set on the promoted spec, no emptied stub is left as a
signpost, and no archived record is rewritten: the archived
`2026-08-08-add-openxwallet` packet and `docs/archive-record-discrepancies.md`
row 7 are ANNOTATED with the carry-forward instead.

## REMOVED Requirements

### Requirement: An agent holder declares its composition

**Reason**: `split-openxwallet-repo` splits the wallet primitives out of `openxFactory` into their own neutral product repository. Under R3 the new repository owns the wallet's own standard — both contract families, the corpus, the validator, the syntax gate and both promoted specs — while `openxFactory` keeps only the seam (`governance/review-authority/`, the trust-anchor / identity-brokering / roles-authority-model compositions and the ideation provenance). The requirement is holder-agnostic, non-substrate product content and belongs to no single layer's corpus, so it is not amended here; it EXITS.

**Migration**: the requirement is promoted unchanged in `opensoft/openXwallet`'s own OpenSpec instance at `wallet-v1.0`, and `openxFactory` consumes it at the commit and per-file digests recorded in `contracts/openxwallet-pin.yaml`. The only prose edit the byte-identity floor permits travels with it: the requirement's subject becomes `openXwallet SHALL` in the new repository, because a requirement naming the repository that no longer holds it is not a pure move either. No `kind:` value, capability id, finding code, filename or path is renamed in v1 (R2).

### Requirement: A composition change revokes the agent's grants immediately

**Reason**: `split-openxwallet-repo` splits the wallet primitives out of `openxFactory` into their own neutral product repository. Under R3 the new repository owns the wallet's own standard — both contract families, the corpus, the validator, the syntax gate and both promoted specs — while `openxFactory` keeps only the seam (`governance/review-authority/`, the trust-anchor / identity-brokering / roles-authority-model compositions and the ideation provenance). The requirement is holder-agnostic, non-substrate product content and belongs to no single layer's corpus, so it is not amended here; it EXITS.

**Migration**: the requirement is promoted unchanged in `opensoft/openXwallet`'s own OpenSpec instance at `wallet-v1.0`, and `openxFactory` consumes it at the commit and per-file digests recorded in `contracts/openxwallet-pin.yaml`. The only prose edit the byte-identity floor permits travels with it: the requirement's subject becomes `openXwallet SHALL` in the new repository, because a requirement naming the repository that no longer holds it is not a pure move either. No `kind:` value, capability id, finding code, filename or path is renamed in v1 (R2).

### Requirement: Agent authority is grant scope, not a parallel vocabulary

**Reason**: `split-openxwallet-repo` splits the wallet primitives out of `openxFactory` into their own neutral product repository. Under R3 the new repository owns the wallet's own standard — both contract families, the corpus, the validator, the syntax gate and both promoted specs — while `openxFactory` keeps only the seam (`governance/review-authority/`, the trust-anchor / identity-brokering / roles-authority-model compositions and the ideation provenance). The requirement is holder-agnostic, non-substrate product content and belongs to no single layer's corpus, so it is not amended here; it EXITS.

**Migration**: the requirement is promoted unchanged in `opensoft/openXwallet`'s own OpenSpec instance at `wallet-v1.0`, and `openxFactory` consumes it at the commit and per-file digests recorded in `contracts/openxwallet-pin.yaml`. The only prose edit the byte-identity floor permits travels with it: the requirement's subject becomes `openXwallet SHALL` in the new repository, because a requirement naming the repository that no longer holds it is not a pure move either. No `kind:` value, capability id, finding code, filename or path is renamed in v1 (R2).
