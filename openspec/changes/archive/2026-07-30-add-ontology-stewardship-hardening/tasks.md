# Tasks — add-ontology-stewardship-hardening

Realized 2026-07-30. Starter v14 (1.1–1.3): `--ontology-only` writes only
the ontology tree + content-manifest declaration and prints the report to
stdout (smoke-verified on a pre-populated repo: 9 files created, foreign
files untouched, no docs/ report); the STARTER marker joins the inventory
and records seeded placeholders structurally; starter suite green with the
v14 assertions. Release tool (2.1–2.3): manifest rewrite carries
`adoption`/`notes`; `--migration-map ../escape.yaml` refused ("resolves
outside the package"); retained snapshots (self-retention AND fallback)
born `lifecycle_state: superseded` — all three probed in the stewardship
suite. Validator (3.1–3.4): starter-provenance is CONTENT (beside-package
marker → ONT-DIGEST "not inventoried"; deleted marker → digest break);
readiness blocks on marker-recorded placeholders (heuristics retained as
defense-in-depth); ONT-RETENTION fails a snapshot claiming an active
lifecycle; ONT-POLICY fails a declared cadence with no external
`review_by` deadline — the rule immediately caught the codex pilot's
undated `example-eng-standard` source (fixed in the pilot answers);
stewardship-policy schema requires min OR max per signal (`anyOf`); four
new negatives (retained-not-superseded, starter-marker-uninventoried,
policy-signal-unbounded, source-no-deadline), corpus 55, ratchet 55 in
the bytes. Gateway (4.1–4.2): the eight semantic fixtures carry probes
(six inline mutations of the canonical packet, executed through the
extracted `packet_semantic_errors` core + packet schema) or `executed_by`
delegates (tenant-binding → the canonical ontology negative;
provider-replacement → the semantic suite), resolution verified;
neutralizing a probe's mutation fails the validator ("probe executed but
the mutated packet was NOT rejected" — sentinel-verified). Corpus +
domains (5.1–5.2): fixtures + pilots regenerated (superseded snapshots,
inventoried markers, v14); MedxFactory f4ca313 and codexFactory 11777a9
inventory their markers and restamp (kernel pins unchanged), both green.
Battery: ontology self-test 10 positives / 55 negatives + repo scan +
determinism; starter/stewardship/semantic/wiring suites; gateway;
MedxFactory make validate; codex repo-mode. `validate-manifest-digests.py`
reports the two changed schema digests stale by design until the v1.24
cut refreshes them.

## 1. Starter (adoption mode + structural provenance)

- [x] 1.1 `--ontology-only`: skip the whole-repo template and README-link stages; run ontology generation, content-manifest declaration, and candidate ingestion; print the rerun report to stdout; instantiation on empty targets unchanged.
- [x] 1.2 The STARTER marker records seeded placeholders (`placeholders: {terms, stewards}`; starter-provenance schema gains the optional block) and joins the package INVENTORY (digest-covered).
- [x] 1.3 `test-domain-starter-ontology.py`: ontology-only probe on a pre-populated repo (only ontology surfaces written, foreign files untouched, no report file); marker inventoried + placeholders recorded.

## 2. Release Tool (F21)

- [x] 2.1 Faithful manifest rewrite: carry `adoption` and `notes`; verified against the schema property list.
- [x] 2.2 Evidence-path containment: `--migration-map`/`--quality-report`/`--consumer-impact` refuse paths resolving outside the package directory.
- [x] 2.3 Retained snapshots born `lifecycle_state: superseded` (self-retention and fallback); stewardship suite asserts all three legs (dropped-field carry, `../` refusal, superseded snapshots).

## 3. Validator Rules (F24/F25/F26 + retention honesty)

- [x] 3.1 Starter-provenance kind becomes package CONTENT (uninventoried marker flagged; deleted marker breaks the digest); readiness blocks structurally on marker-recorded placeholders (string heuristics retained as defense-in-depth).
- [x] 3.2 `ONT-RETENTION`: a retained manifest whose `lifecycle_state` is not `superseded` fails.
- [x] 3.3 Cadence rule: policy `source_review` + external-kind source without `review_by` → finding.
- [x] 3.4 Stewardship-policy schema: required signal declares `min_value` OR `max_value` (`anyOf`); new negatives (retained-not-superseded, marker-uninventoried, signal-unbounded, source-no-deadline) and the corpus minimum ratchets accordingly.

## 4. Gateway (F27)

- [x] 4.1 Conformance fixtures gain `probe` (mutations of the canonical example packet) or `executed_by` (resolution-verified delegate); the eight semantic ids covered — six probed inline, tenant-binding and provider-replacement delegated.
- [x] 4.2 `validate-memory-gateway.py`: preflight core extracted to run over a single packet; probes executed (expected rejection asserted); dangling delegates fail.

## 5. Corpus, Domains, Release, Archive

- [x] 5.1 Regenerate fixtures + pilots under the new semantics (superseded retained manifests, inventoried markers); full battery green.
- [x] 5.2 MedxFactory + codexFactory follow-on commits: inventory the STARTER marker, restamp (kernel pins unchanged), validate green, push.
- [x] 5.3 Cut contract-v1.24 (two schema digests refreshed; the cut carries the recorded v1.23 erratum correction — note it in the CHANGELOG entry), tag, remote-verify.
Reviewer verification (5.4, at 55a6202): every finding re-tested by
construction — F21(a) adoption/notes survive a real pilot release; F21(b)
all three evidence flags refuse `../../` escapes; F21(c) snapshots born
superseded, a hand-flipped snapshot fails, and the F3 seal re-verified
independently (13 snapshots, per-file sha256 + reproduced digests, 0
bad); F24 blocks on the recorded identifier (label-rename attack still
blocks; the reviewer's original no-name-steward bypass is structurally
gone); F25 both directions (deleted marker → digest break; de-inventoried
marker → flagged); F26 anyOf behaves exactly (max-only PASSES, neither
fails) and the cadence rule fires; F27 "resolved, and better covered than
claimed" — neutralizing the probe applier showed ALL SIX probes
load-bearing, a single-probe neutralization names exactly that fixture,
dangling delegates fail. Adoption mode verified against a pre-populated
repo incl. additive content-manifest merge preserving a pre-existing
content kind. Bundle v1.24 recomputed (179 entries, 0 mismatch) and
DELIVERS the v1.23 erratum correction; manifest digests 104/104; ratchet
55 in the bytes with guide/README counts corrected ("third time asked" —
closed). Corpus audit 55 negatives 0 rot / 10 positives 0 failures.
Verdict: **APPROVED for archive at 55a6202**. One non-blocking
observation carried forward: MedxFactory (f4ca313) and codexFactory
(11777a9) hold `starter_version: 13` markers without the `placeholders`
block — inventoried per F25 but not regenerated at v14; both are draft
and correctly refuse readiness, so this is scaffold hygiene, folded into
whichever change first drives a real domain toward publication (the
kernel-publication / domain-publication line).

- [x] 5.4 Reviewer verification of F21/F24–F27 + the adoption mode against the release candidate; docs updated (family README, guide, versioning notes); archive with README moved Active → Archived.
