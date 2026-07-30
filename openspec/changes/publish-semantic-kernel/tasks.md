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
- [ ] 6. Reviewer capstone verification of the publication against the release candidate; archive on green evidence with README updated.
