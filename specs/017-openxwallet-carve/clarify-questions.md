# Clarification round — feature 017-openxwallet-carve

**Path**: `/home/brett/projects/xFactory/openxFactory-worktrees/P2-openxwallet-carve/specs/017-openxwallet-carve/clarify-questions.md`

**Session**: 2026-08-26 · **Status**: resolved without blocking

The ratified change `split-openxwallet-repo` decided every question this feature
could have asked: the twelve path sets, the byte-identity floor and its one named
prose carve-out, R1–R8, D7/D8/D12–D14, and clarifications N1/N3/N8. The scan
below therefore found **no critical ambiguity in the spec**.

Three points of FACT, however, turned out to differ from what the ratified design
and the launching brief assumed about the current openxFactory tree. Each is
recorded here with the resolution taken, so the divergence is auditable rather
than silent. **None blocked; none was put to a human.**

---

## Q1. openxFactory's manifest row for the envelope schema carries NO `sha256`

**Context.** Task 3.12 and design D7 (N8) require openXwallet's CONSUMED-member
row to carry a `sha256` "EQUAL to the pinned openxFactory row's". Read at the
carve commit, openxFactory's row for
`contracts/schemas/hermes-job-envelope.schema.yaml` carries `id`, `path`,
`source_path`, `type`, `schema_version`, `intended_consumers`,
`compatibility: copied_from_source_commit` and
`adapter_owner: Omnigent-Install` — **and no `sha256` field at all**. The
artifact is content-addressed by commit from `opensoft/Omnigent-Install`, so
there is no recorded digest to copy.

**Resolution taken.** The `sha256` is COMPUTED over the vendored bytes at the
NAMED CARVE COMMIT — which is the digest of the pinned openxFactory artifact,
just recomputed rather than transcribed. The row carries a comment saying so, and
`contract_pin.yaml` carries the same value, so the verify step compares
recomputed against recorded exactly as ratified. The intent of "equal to the
pinned row's" — that the digest identify the pinned bytes — is met; the letter
("copy the recorded value") is unsatisfiable because no such value exists.

## Q2. The upstream `adapter_owner` for that artifact is `Omnigent-Install`

**Context.** D7 (N8) ratifies `adapter_owner: openxFactory` on openXwallet's
consumed row. openxFactory's own row names `Omnigent-Install`.

**Resolution taken.** The RATIFIED value stands: `adapter_owner: openxFactory`,
because openxFactory is who openXwallet pins and who owns the copy openXwallet
consumes. The upstream chain is carried as a comment on the row and as
`source_path`, so the two-hop provenance (Omnigent-Install → openxFactory →
openXwallet) is readable without weakening the ratified field.

## Q3. Which checks the new ruleset requires

**Context.** Task 3.27's evidence names `required_status_checks →
[wallet-validation]`; the launching brief names `[wallet-validation,
pytest-suite]`. Read at the carve commit, openxFactory ruleset **21538893** — the
one D8 says to mirror — requires **both** tokens (updated 2026-08-26 17:39).

**Resolution taken.** Both tokens are required, which mirrors 21538893's actual
shape and satisfies task 3.27 (the named token IS required). The addition is
recorded rather than assumed; it is strictly stronger than the named minimum and
weakens nothing.

---

## Coverage scan

| Category | Status |
| --- | --- |
| Functional scope & behavior | Clear — ratified group 3, 31 tasks |
| Domain & data model | Clear — twelve path sets, eight owned rows, one consumed |
| Interaction & UX flow | Clear — the operator's ordered phases (D8) |
| Non-functional quality | Clear — the gates ARE the quality attribute |
| Integration & dependencies | Clear — `git filter-repo`, `gh`, the pin in both directions |
| Edge cases & failure handling | Clear — case-variant collision, rename hazard, mutated pin |
| Constraints & tradeoffs | Clear — R1–R8 LOCKED, byte floor, one carve-out |
| Terminology & consistency | Resolved — `openXwallet` per Amendment 2 (PR #396) |
| Completion signals | Clear — SC-001..SC-009 |
| Misc / placeholders | Resolved — Q1–Q3 above |

**Recommendation**: proceed to `/speckit-plan`. No question is outstanding.
