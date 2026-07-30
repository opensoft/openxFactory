# Tasks — add-ontology-term-lifecycle-enforcement

Realized 2026-07-30. Validator (1.1–1.4): `ONT-TERM-LIFECYCLE` +
`ONT-TERM-VERSION` registered in the docstring and family README; the
prior-revision comparison loads retained terms for EVERY compatibility
class (edge rubric stays gated to non-breaking); forward-only lifecycle
via `LIFECYCLE_ORDER`, meaning-bearing fields per kind (concepts:
label/aliases/definition/parents; relations: + domain/range/
characteristics), backward `effective_version` rejected; retired terms
rejected in profile `required_terms` (kernel-resolving) and in
current-digest context subsets, prior-pin contexts untouched. Tools
(2.1–2.2): `ontology-release.py` refuses publication naming draft terms
(deprecated/retired transitions exempt); `ontology-compile-context.py`
refuses retired terms in the requested set or computed closure (verified
live against the retired `xf/codex/decomposition`). Fixtures/pilots/tests
(3.1–3.4): five new negatives (draft-term-in-published, term-resurrected,
term-changed-no-bump, profile-requires-retired, context-includes-retired),
minimum ratcheted 44 → 49; pilots publish seeded terms as an explicit
steward act before first release and bump the reparented medx term to
0.2.0; stewardship suite probes the draft refusal then publishes and
proceeds. Battery green: self-test 10 positives + 49 negatives, repo
scan, determinism, three suites, memory gateway, both pilots
ontology_ready, MedxFactory `make validate`, OpenSpec 58/58 strict.

- [x] 1.1 Add `ONT-TERM-LIFECYCLE`: a `published`/`deprecated` package containing a `draft` concept or relation fails; register the code in the validator docstring and the family README table.
- [x] 1.2 Restructure the prior-revision comparison to load retained previous terms for EVERY compatibility class; keep the existing removal/parent/range edge rules gated to non-breaking classes.
- [x] 1.3 Enforce forward-only term lifecycle across revisions (`draft → published → deprecated → retired`, skips allowed) as `ONT-TERM-LIFECYCLE`; enforce meaning-bearing-change-requires-bump and no-backward `effective_version` as `ONT-TERM-VERSION`.
- [x] 1.4 Reject a retired term in an inventoried worker profile's `required_terms` and in the subset of any context pinned at the CURRENT package digest (`ONT-TERM-LIFECYCLE`), leaving prior-pin contexts untouched.
- [x] 2.1 `ontology-release.py`: refuse `--lifecycle published` (the default) while any term is `draft`, naming each draft term; `deprecated`/`retired` transitions are exempt.
- [x] 2.2 `ontology-compile-context.py`: refuse a retired term in the requested set or the computed closure, naming it; deprecated terms stay compilable.
- [x] 3.1 Five new indexed negatives — draft-term-in-published-package, term-resurrected (paired-revision), term-changed-no-bump (paired-revision), profile-requires-retired-term, context-includes-retired-term — and ratchet the self-test minimum 44 → 49.
- [x] 3.2 Pilots: publish seeded terms as an explicit steward act before first release; bump the reparented medx term's `effective_version`; keep the codex retirement flip; regenerate the corpus and pilots green.
- [x] 3.3 `test-ontology-stewardship.py`: probe the draft-term publication refusal, then publish terms and proceed; full battery (self-test + repo scan + determinism + suites + gateway + MedxFactory validate + OpenSpec strict) green.
- [ ] 3.4 Update the family README (codes table, fixture counts) and the guide's proof-surfaces line; reviewer verification of F18 against the release candidate; archive on merged + green realization evidence (target_release: none).
