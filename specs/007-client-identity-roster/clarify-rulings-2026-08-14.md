# Architect rulings — 007-client-identity-roster clarify round 1

Date: 2026-08-14. Seat: architect (main session).
Status: **reviewed** — cross-model adversarial review completed 2026-08-14;
verdicts: 2 upheld, 5 amended (adopted below), 4 broken (superseded below).
Two points escalated to Brett as genuine ratified-scope decisions — see
"Escalated" at the end; their outcomes are recorded there once ruled.

Ground rule unchanged: the five ratified answers and the two killed flaws are
fixed points.

## Final rulings (post-review)

**R1 (amended) — fragment placement = `credentials/client-identity-roster/<client_ref>.yaml`**
in the domain repo, inside the tree `validate-credential-contracts.py` scans
(verified: it scans `<repo>/credentials` recursively and prints a skip-with-
notice for unknown kinds — the promoted credential-contracts spec blesses
this, so the roster's consumption rule notes the notice is expected).
ADDITIONALLY: the canonical roster validator SHALL sweep the entire target
repo for `kind: xfactory_client_identity_roster` and report any instance
outside the declared placement as a **misplacement finding** — placement is
mechanized, not advisory. (Corrected rationale: `tenants/` is scanned by
OpsxFactory's own validator for examples; the point is that no kind-aware
validator covers a stray fragment, not that no validator scans the path.)

**R2 → ESCALATED (Decision A).** The adversarial review showed pack
membership is mandated by the ratified proposal (proposal.md:171-172) and
design (design.md:114-116) — not the sketch — and that pack membership is the
ONLY promoted mechanism conferring blocking status (sole hit:
`openspec/specs/domain-conformance-checks/spec.md:16`); domain gates invoke no
canonical validator today, and domain-repo edits are out of scope here
(FR-030). Dropping pack enrollment would be a ratified-scope reduction. Since
the promoted pack spec enumerates three scripts exhaustively, enrollment
requires a `domain-conformance-checks` MODIFIED delta the proposal does not
declare. Cure = declare it (Brett) — see Decision A.

**R3 (amended) — doc-health count: code lands 16 now; promoted text rewrites
at archive.** Verified: no automated count assertion; README already says
"sixteenth family" while promoted text says fifteen, green today. The spec's
FR-025 and SC-009 SHALL be reworded to require agreement with the **ratified
delta wording** (promoted text is rewritten by the archive step), and the
feature updates the prose sites it owns — at minimum
`scripts/doc_health/families.py:1` ("The fifteen contract check families.").

**R4 → ESCALATED (Decision B) for the neutral home; split itself upheld.**
Verified: NO neutral `issuance_preconditions` vocabulary exists — the
mechanism is a domain-local extra key in OpsxFactory's requirements.yaml
riding a neutral schema that neither declares it nor forbids extras. Giving
the refusal any neutral home means modifying `credential-contracts` — an
undeclared third capability (same defect class as Decision A). See Decision B.
Regardless of B's outcome: SC-008 SHALL be reworded so the neutral criterion
is a conformant requirement-record **fixture** declaring the roster-drift
precondition (no live producer of drift findings exists at archive time —
state this explicitly in the spec); live refuse/allow is proven in the domain
follow-up at the domain mint surface.

**R5 (superseded) — NO completeness rule in the first release.** The review
proved the invented predicate fires permanently on 14 of OpsxFactory's 16
requirement classes, including classes the ratified clarify answers place
outside roster scope verbatim, and demanding an entry for
`microsoft_endpoint_destructive_external` re-admits killed flaw (b). The
packet defines no completeness rule; inventing one on a BLOCKING check is
scope creep. FR-032 SHALL be rewritten: no completeness enforcement in v1;
absence of a fragment or of an entry is never a finding (permissive axis,
ratified answer 3); FR-031 and the out-of-scope-surface edge case are RETAINED
as guards. Scoped completeness (factory-held identity classes on first-release
surfaces in client tenants with issued grants) is recorded as a NAMED
SUCCESSOR change, not built here.

**R6 (upheld) — no admission-freshness decay in v1.** `verified_at` recorded;
verified vs unverified is the only distinction.

**R7 (amended) — vocabulary closedness + the alias rule.**
`admission_surface` CLOSED (`business_central|exchange`), `residency_model`
CLOSED, `enforcement_mode` CLOSED (its two members named explicitly in the
schema), `identity_kind` CLOSED with members taken VERBATIM from the ratified
delta / task 2.1 field list — if the packet does not enumerate them, the
members are exactly the kinds appearing in the four mandated examples, closed
at that set for v1 (the builder invents no unratified vocabulary).
`blast_radius_unit` and `duty` are domain-declared tokens, pattern-bound
(`^[a-z0-9][a-z0-9_-]*$`), each declared once in a fragment legend that BINDS
the token to its provider-native identifier (e.g. `sandbox1` → `Sandbox1`) —
provider fidelity lives in the legend, `granted_permissions[]` and
`achieved_scope` stay provider-native.
ALIAS RULE (threads both walls): a finding is raised ONLY when two entries
differ solely in a free token AND are observationally identical — same
`granted_permissions[]` set and same admission acts (surface, act,
`achieved_scope`, `enforcement_mode`) — AND no duty-separation rationale is
declared. Genuine per-unit pairs differ in `achieved_scope`; genuine duty
pairs differ in permissions or declare the rationale. Killed-flaw acceptance
fixtures MUST include a genuine per-unit pair and duty pair passing with zero
findings alongside one alias-pair negative.

**R8 (superseded) — drift finding is a governed record in the roster contract
family**, own `kind` + `schema_version`, carrying: identity_ref (the
five-element uniqueness tuple), fragment_ref, rule id, **`roster_value`**,
**`observed_value`** (both mandated by the ratified delta scenario
"records the roster value and the observed value"), `observed_at`,
`opened_at`, `status: open|resolved|disposed`, disposition citation. Borrow
doc-health FIELD NAMES where they apply; do NOT claim alignment with a
doc-health findings register (none exists — doc-health is stateless
recompute; `health/dispositions.yaml` is advice text, not an on-disk record).
The refusal (per Decision B) consumes this record deterministically.

**C1 — falls/rises with Decision A.** Until ruled, FR-022 stays as the
ratified text (pack, blocking) with a `[PENDING DECISION A]` marker.

**C2 (amended) — archive blockers.** Contract records + consent-instrument
cascade (task 3.2) + doc-health sixteenth family (task 3.4) + task 3.1 (pack,
subject to Decision A) + the neutral refusal fixture (task 3.3, subject to
Decision B). "Both wirings" in task 5.3 denotes 3.2 + 3.4 (the two declared
Modified Capabilities); 3.1 and 3.3 are dispositioned by Decisions A and B,
not by silence. Only section 4 (domain fragments) is exempt from archive.

**C3 (upheld, rationale corrected) — `examples/client-identity-roster/`.**
The tree carries TWO conventions: `examples/<family>/` when the schema lives
in `contracts/schemas/` (this one does, per task 2.1); `contracts/<family>/examples/`
when the family owns a contracts subdir (006/openxwallet — do not "fix"
toward it). Include a `negative/` subdir and a README like sibling families.
The four mandated cases span at least TWO fragment files (fragments are per
(client, domain); task 2.3 demands a two-domain client).

## Rulings on the review's new issues

**N1 — `withdrawn`:** grow the closed consent-instrument `status` enum by
`withdrawn` (the delta text requires behavior on "terminated or withdrawn";
consent-instrument IS a declared MODIFIED capability). The cascade check
fires on both. No aliasing — withdrawal and termination are distinct events.

**N2 — enum growth mechanics:** follow the schema's own stated rule — bump
consent-instrument's `contract_schema_version`; register the new schema
row(s) at contract-v1.32 with `compatibility` declared per existing manifest
conventions (read the last bump's rows and copy the shape); FR-030 "existing
suites unaffected" is honoured by additive growth + this feature updating the
consent validator/fixtures it is declared to modify.

**N3 — credential-contracts as hidden third MODIFIED capability:** that IS
Decision B.

**N4 — name collision:** the new doc-health family module and family id MUST
NOT collide with `scripts/doc_health/shared_identity.py` (active
`add-shared-identity-seeds` lane). Unless the ratified delta names a family
id, use `client-identity-composition` (module
`client_identity_composition.py`); "shared identity material" remains a
finding CLASS inside it, not the family name.

**N5 — misplacement:** mechanized in R1 (whole-repo kind sweep).

**N6 — no drift producer at archive:** folded into R4/SC-008 rewording —
fixture-proven, stated explicitly.

**N7 — evidence_ref semantics:** `evidence_ref` is a declared pointer
(repo + path, optionally sha), NOT resolved by the canonical validator
(network-free, single-repo). Resolution is checked only by the cross-domain
doc-health family, which assembles from pinned repos. FR-011's
gate-obligation resolution requirement is unchanged. STALE SEED FACT
corrected: the BC evidence chain IS on OpsxFactory main (c1a6270 verified an
ancestor of origin/main — PR #19 merged), so packaged-example refs point at
real pinned content.

**N8 — bundle version:** contract-v1.32 confirmed against
`contracts/manifest.yaml` (v1.31 today). No action.

## Escalated to Brett

**Decision A — pack enrollment (ratified deliverable vs undeclared
modification).** The ratified proposal/design mandate the roster check join
the `domain-conformance-checks` pack (blocking), but the promoted pack spec
enumerates three scripts exhaustively and the proposal does not declare that
capability modified. Options: (i) AMEND the ratified change — add a
`domain-conformance-checks` MODIFIED delta (pack grows to four; the check
passes-with-notice in repos with no roster fragment, per R5), update the
proposal's Modified Capabilities, re-validate strict, record the amendment in
the decision review. (ii) REDUCE scope — move pack enrollment to a named
successor; answer 2's blocking clause is unrealized at archive.
Architect recommends (i).

**Decision B — the refusal's neutral home.** Options: (i) AMEND the ratified
change — declare `credential-contracts` MODIFIED, adding the
`issuance_preconditions` vocabulary (with the roster-drift member) to the
neutral schema; fixture-proven per R4. (ii) route the vocabulary through the
active `add-dispatch-credential-contract` change (cross-lane coupling).
(iii) REDUCE — refusal stays a domain-local key; the neutral layer ships
nothing; answer 2's third clause is domain-realized only.
Architect recommends (i).

**Outcome (Brett, 2026-08-14):** Decision A = AMEND (option i) — add the
`domain-conformance-checks` MODIFIED delta, pack grows to four, blocking stays
an archive blocker. Decision B = AMEND (option i) — declare
`credential-contracts` MODIFIED, the neutral schema gains the
`issuance_preconditions` vocabulary with the roster-drift member,
fixture-proven at the neutral level. Both amendments are recorded in the
packet's decision review and re-validated strict before encoding.
