# Plan-gate rulings — 007-client-identity-roster

Date: 2026-08-14. Seat: architect. Input: the cross-model adversarial review
of plan.md/research.md at `913c3ca` (17 decisions: 11 upheld, 5 amend,
1 broken; 4 new issues; packet re-amendment NOT needed).
Status: **ruled** — apply all of the following to plan.md/research.md.

Most rulings ADOPT the reviewer's own minimal amendments verbatim; only R-N1
is a fresh architect ruling and carries its own verification obligation.

## R-N1 (fresh ruling) — uniqueness tuple element 3 = `authority_class_intended`

The five-element key is (domain, admission_surface, **authority_class_intended**,
blast_radius_unit, duty). Rationale: a key must be declarative and stable —
`achieved` is observational and moves with provider state, so keying on it
would change an identity's identity when drift occurs, which is incoherent
(drift is what FR-009/FR-010 REPORT about a stable identity, not what
re-keys it). The drift record's `identity_ref` object carries the same
intended value as its stable join key; observed values ride
`roster_value`/`observed_value`.
VERIFICATION OBLIGATION (cross-model, before encoding): sweep every ratified
mention of the uniqueness key (spec.md FR-005/FR-006/Key Entities, the roster
delta, design.md, the seed's killed-flaw block) — if ANY text implies the
achieved class participates in uniqueness, STOP and report instead of
encoding. Encode `$defs.identity_key` accordingly and say explicitly in both
plan.md and research.md that intended was chosen and why.

## Adopted amendments (reviewer's minimal fixes, applied as stated)

- **A-2 (decision 2):** both kinds in the roster schema file declare
  `schema_version: const: 1`, stated in plan.md, so the single manifest row is
  unambiguous.
- **A-3a (decision 3):** `issuance_preconditions` values are `const: true` in
  the neutral schema AND the canonical validator raises a `_semantic_findings`
  entry for a false-valued or out-of-vocabulary member — the semantic mirror
  is structurally required because self-test negatives adjudicate against
  `_semantic_findings` only (decision 4's verified fact).
- **A-3b (decision 3):** each of the three members carries a one-line schema
  `description` naming its governed condition; the two precedent members cite
  `adopt-deployment-handoff-boundary`.
- **A-5 (decision 5):** the `governed_identity` dependent-ref's `ref` names
  the roster fragment path plus the entry's `identity_ref`, UNRESOLVED by the
  validator (FR-037 posture), stated in the schema description.
- **A-6 (decision 6):** delete the false sentence "existing
  termination-without-cascade-evidence code is unchanged in meaning";
  restate as "reach widens to `withdrawn`; the code spelling is retained for
  continuity."
- **A-11 (decision 11, BROKEN → fixed):** two additions to the fixture plan:
  (1) a FOURTH repo-shaped fixture whose entry's gate obligation names a gate
  absent from that fixture's `workflows/` — homes FR-011's "unresolvable
  obligation" negative; (2) a packaged negative
  `achieved-class-contradicted-by-permissions.yaml` — homes FR-004's rule.
  Re-count FR-016's per-rule negative coverage after both and state the
  count.
- **A-7 (decision 7 note):** record as a verified precondition that no consent
  class registry in the estate aliases a key spelled `withdrawn` (swept
  2026-08-14), so narrowing `alias-remaps-neutral-status` fires nowhere.
- **A-9 (decision 9 note):** name the trap — `tests/doc-health/conftest.py`
  `make_ctx` defaults `agg_root=None`; every fixture test must pass `agg_root`
  explicitly or the family short-circuits into its first skip.
- **A-16 (decision 16):** the multi-surface reader's citable provider fact
  becomes a PRECONDITION verified before Cluster D begins, not a discovery
  inside it; if no in-vocabulary citation exists, STOP and escalate to the
  architect with the candidates (do not synthesize a fact).
- **A-N2 (new issue 2):** plan.md records the residual honestly: pack
  blocking is nominal at archive — codexFactory's gate enumerates three
  members by name and OpsxFactory's gate invokes no canonical checks — and
  the domain-gate wiring joins the named follow-ups (it is a domain-repo
  edit, out of scope per FR-030/SC-012).
- **A-N3 (new issue 3):** fix the false claim at plan.md:62 — a one-member
  `admission[]` array IS a legal single-act expression; only the scalar form
  is unrepresentable. (An implementer reading it literally would write
  `minItems: 2` and break legitimate entries.)
- **A-N4 (new issue 4):** SC-006 is proven across BOTH corpora: state that the
  canonical roster validator also runs over the doc-health cross-domain
  fixture repos and exits 0.

## Not escalated to Brett

Nothing here changes ratified scope: R-N1 resolves an ambiguity both readings
of which live inside the ratified key; everything else adopts
reviewer-verified minimal fixes. The A-16 escalation path exists but has not
triggered.
