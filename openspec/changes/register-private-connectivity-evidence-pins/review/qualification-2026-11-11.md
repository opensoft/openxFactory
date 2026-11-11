# Pin-register qualification: 2026-11-11

Status: record

The narrow repair is implemented and qualified. The shared reader declares the feature's root-local and foreign-owner inventory fields; required regression checks preserve local reachability and explicit source ownership. No evidence path is excluded.

The [immutable qualification record](https://github.com/opensoft/openxFactory/blob/50cafafa73351e6141cde07e39e41e427b75e6f8/specs/040-private-connectivity/evidence/pin-register-qualification.json) records the tested sources and all successful required checks. The published implementation before this sign-off update passed 152 local tests plus 52 subtests, five subsequent ownership/census checks, 2,160 tests in the Python 3.14 doc-health suite and 10,373 tests plus 735 subtests in the full required pytest suite. Its measured standing census was 541 sites and 31 members. New approval records add declared sites; the final committed census and evidence chain are revalidated with this update.

Original physical measurements, current runtime pins and explicit component comparisons remain distinct. No full pilot or binary upgrade rerun is claimed for this bookkeeping update.

Brett Heap's [revised five-role lab approval](https://github.com/opensoft/openxFactory/blob/50cafafa73351e6141cde07e39e41e427b75e6f8/specs/040-private-connectivity/evidence/G4-repair-approval.json) completes the human G4 gate. All six implementation pull requests remain draft. GitHub CI, Codex review and commercial release authority remain separate; the latest Codex review requests reported a quota limit, which is not recorded as a passed review.

After recording the five-role sign-off, the final feature/pin-register regression run passed 152 tests plus 52 subtests, and the committed census measured 552 sites and 31 members. All 20 task evidence records verify, all 21 Spec Kit tasks are checked complete, all 224 immutable file references resolve, and the 244-row corpus ledger is consistent. See [the final validation log](../../../../specs/040-private-connectivity/evidence/G4-signoff-validation.txt).
