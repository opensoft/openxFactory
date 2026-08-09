# Tasks: add-composed-view-authoring

## 1. The serve declares what it can write

- [x] 1.1 `/capabilities` reports `repository`, resolved per request from
      `_session_repository()` — the same authority `refuse_foreign_repository`
      compares against, so the capability and the refusal cannot disagree.
      Resolved per request rather than at startup because the registry that
      answers it is not populated when the capability dict is built.

## 2. One affordance asks the serve, not the view

- [x] 2.1 `app.js` threads the UNSTRIPPED probe and the declared repository to
      the lens and to the workbench's `openDraft`. Every other surface keeps
      the stripped capabilities unchanged.
- [x] 2.2 The lens offers the hand-off when the SERVE can create and a
      writable repository is declared; the jump and the stated reason remain
      for when it cannot.
- [x] 2.3 The create seed names the declared repository, never the project id.

## 3. Verification

- [x] 3.1 Live from the merged `domains` project: the hand-off is offered and
      doxBench opens with `Repository context: openxFactory` (it read
      `domains` before, which the route would have refused).
- [ ] 3.2 Brett creates the first real document from a project view — the
      write itself is his to make, not something to exercise against his
      checkout unasked.
