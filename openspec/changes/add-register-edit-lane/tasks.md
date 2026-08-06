# Tasks: add-register-edit-lane

## 1. The lane

- [x] 1.1 `register_edit_lane.py`: scan dispatched `project-register-edit`
      descriptors (both project verbs); surgical block edits on the register
      (create appends a project; edit adds/removes members inside the
      project's block; comments preserved); pinned-schema validation BEFORE
      writing; structured `delivered_at`/`delivered_by` stamps on the flip;
      refuse-and-report for stale commissions.
- [x] 1.2 Git half: commit ONLY `project-register.yaml` (explicit pathspec)
      and push with pull-rebase-retry; any git failure leaves the file
      edited, the descriptor dispatched, and reports.
- [x] 1.3 CLI: `python3 -m ideation_dashboard.register_edit_lane
      --repo-root . [--watch --interval N] [--no-git]`.

## 2. The button

- [x] 2.1 `POST /actions/apply-register-edits`: loopback-only, gate-actor
      required; runs the lane once, returns the report.
- [x] 2.2 Header affordance: "⟳ apply N pending" whenever the projection
      carries pending items under the gate capability; reloads on success.

## 3. Verification

- [x] 3.1 Lane tests: create/add/remove applied on a comment-bearing fixture
      register (including the empty-list form), validation refusal, stale
      commission refusal, delivered stamps, git-off mode.
- [x] 3.2 Wire test: commission → apply route → register updated, descriptor
      delivered, report shape; refused off-loopback.
- [x] 3.3 Live browser check: the button appears with a pending commission,
      applies it, and the projection's truth plane reflects the edit; zero
      page errors.
      (Verified 2026-08-06 on a scratch git fixture — bare remote + clone +
      register + fixture corpus: the filter's add dropdown commissioned
      repoB into core; after reload the header read "⟳ apply 1 pending";
      the click ran the lane in the serve — the register gained repoB, the
      register-only commit landed AND pushed to the remote, the shell
      reloaded, and the button retired with nothing pending. Zero console
      errors, page errors, and >=400 responses.)
- [x] 3.4 Runbook: the watcher's run line beside the serve.
- [ ] 3.5 First unattended fulfilment observed (Brett commissions; the
      watcher or button delivers with no terminal session involved).
