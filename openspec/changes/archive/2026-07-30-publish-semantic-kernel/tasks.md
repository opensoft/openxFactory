# Tasks — publish-semantic-kernel

Realized 2026-07-30. The steward act (task 1) published all 34 kernel
terms (25 concept entries + 9 relations; meaning-bearing fields and
effective_versions untouched) and restamped the kernel. The governed
release (task 2): `ontology-release.py` published `xf/core` 0.1.0 → 1.0.0
(additive, line `xf/core@1` preserved) decided by
`openxfactory-maintainers` (accountable council) — the release record
sits beside the kernel, both retained snapshots (0.1.0 and 1.0.0) are
born `lifecycle_state: superseded`, and the package-level adoption block
survived the manifest rewrite (the exact F21 kernel scenario, now
exercised in production). Published digest `37090ba2…369038` (content
identical to the post-steward-act 0.1.0 state — publication changed
lifecycle and version, never meaning). Downstream (task 3): fixture
corpus + pilots + gateway examples regenerated against the published
kernel (the generator reads the kernel pin live); the omnigent install
example re-pins kernel 1.0.0 @ the new digest; battery green — ontology
self-test 10 positives / 55 negatives + repo scan + determinism,
starter/stewardship/semantic/wiring suites, memory gateway, omnigent
suite, OpenSpec 58/58 strict. Consumers (task 4): MedxFactory d01ae62 and
codexFactory de60c0c re-pin `kernel_import` to the published digest
(one-line manifest changes; both repos validate green).

- [x] 1. Per-term steward act: all 34 kernel terms `draft → published` (meaning-bearing fields untouched); restamp the kernel.
- [x] 2. Governed release 0.1.0 → 1.0.0 (additive) via `ontology-release.py` as `openxfactory-maintainers`: release record beside the kernel, both snapshots born superseded, adoption block carried through the rewrite.
- [x] 3. Regenerate the fixture corpus, pilots, and gateway examples against the published kernel; update the omnigent install example's kernel pin; full battery green.
- [x] 4. Re-pin MedxFactory and codexFactory `kernel_import` to the published digest (one-line manifest changes); both repos validate green; push.
- [x] 5. Cut contract-v1.25 (three kernel digests refreshed, section comment updated to published 1.0.0, CHANGELOG decision record), tag, remote-verify; manifest digests 104/104.

Capstone verification (task 6, two rounds): round 1 at ac1efd2 confirmed
the publication SOUND on every gate (34/34 terms published with adoption
evidenced incl. relations; the adoption gate broken in place and watched
fail closed; meaning untouched — every effective_version still 0.1.0;
package adoption structurally identical through the rewrite; accountable
council identity; both seals recomputed; 60 downstream pins + 10 contexts
on the published digest; bundle 179/179) and BLOCKED on two false
statements in the record: P1 (an orphan snapshot asserting the LIVE
version superseded, with retention never checked in reverse) and P2 (both
consumers declaring version 0.1.0 behind the content-identical 1.0.0
digest), plus riders P3 (stale DRAFT notes) and P4 (24-vs-25 concept
count — the third stale-count slip, "worth a lint"). The P-wave (ce95d27
+ Medx 516bac9 + codex 6f037d5) resolved all four: retention made
TRUTHFUL IN BOTH DIRECTIONS via the open change's
domain-ontology-lifecycle delta (active snapshot states published;
supersession flips exactly one line — verified by the reviewer as a
2-line diff with the seal intact; orphans and live-superseded claims
fail; the reviewer's deletion preference was declined for the F3
deadlock it would have re-created, and round 2 records "they were right
and I was wrong"); kernel-import checks version AND digest
(kernel-import-version-drift negative); notes corrected without
disturbing the package digest; counts corrected everywhere current and
the COUNT LINT added (README fixture count, pinned minimum, kernel term
counts vs the bytes; NEGATIVE_RATCHET single constant) — it caught its
author's own stale counts on introduction. The kernel-stewardship-policy
question became an explicit ratified scoping decision with a reopening
trigger ("explicit scoping — not omission"). Round 2 at ce95d27:
workspace-wide truthfulness audit (10 packages, zero orphans), the flip
simulated byte-for-byte, post-tag doctrine confirmed correctly applied
(v1.25 tag internally true 179/179), 57 negatives 0 rot / 10 positives 0
failures. Verdict: **APPROVED for archive at ce95d27, no new findings**.
Carried forward (non-gating): the two consumers' v13 markers gain the
placeholders block at their publication-driving change.

- [x] 6. Reviewer capstone verification of the publication against the release candidate; archive on green evidence with README updated.
