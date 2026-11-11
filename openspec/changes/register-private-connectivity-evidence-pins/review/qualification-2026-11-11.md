# Pin-register qualification: 2026-11-11

Status: record

The narrow repair is implemented and qualified. The shared reader declares the feature's root-local and foreign-owner inventory fields; required regression checks preserve local reachability and explicit source ownership. No evidence path is excluded.

The [immutable qualification record](https://github.com/opensoft/openxFactory/blob/50cafafa73351e6141cde07e39e41e427b75e6f8/specs/040-private-connectivity/evidence/pin-register-qualification.json) records the tested sources and all successful required checks. The published implementation before this sign-off update passed 152 local tests plus 52 subtests, five subsequent ownership/census checks, the Python 3.14 doc-health suite and the full required pytest suite. Its measured standing census was 541 sites and 31 members. New approval records add declared sites; the final committed census and evidence chain are revalidated with this update.

Original physical measurements, current runtime pins and explicit component comparisons remain distinct. No full pilot or binary upgrade rerun is claimed for this bookkeeping update.

Brett Heap's [revised five-role lab approval](https://github.com/opensoft/openxFactory/blob/50cafafa73351e6141cde07e39e41e427b75e6f8/specs/040-private-connectivity/evidence/G4-repair-approval.json) completes the human G4 gate. All six implementation pull requests remain draft. GitHub CI, Codex review and commercial release authority remain separate; the latest Codex review requests reported a quota limit, which is not recorded as a passed review.
