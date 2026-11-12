# Review correction: conditional lane attribution

Status: candidate realization of an existing approved policy, 2026-11-11.

openXwallet #48 exposed an old required lane-line check that rejects unlaned
work. Brett's in-force lane-collision Amendment 21 (2026-09-30) already permits
missing attribution outside a lane. The current instruction to resolve findings
commissions this realization; no lane, registration or approval grant is invented.

Precedent: factory change honor-conditional-lane-attribution / feature 041 at
6bfa67887eeba17e13a2553354a639fe56753084. This is repository-local, not a shared
published workflow. Port only its conditional shell and 21 behavior/structure
tests, preserving the adapter's existing job-level Bot exemption, events,
permissions and check token.

Recorded before the workflow edit. The sole implementation list remains adapter
feature 016 tasks T010/T011. The factory binding profile remains draft.
