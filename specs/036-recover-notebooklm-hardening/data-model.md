# Boundary model

Status: draft

- NotebookRow: identity and observed title, parsed once at provider boundary.
- SourceRow: identity, observed title and existing optional provider fields.
- BookSpec: lifecycle key, alias and title; immutable.
- Projection manifest: notebook identity plus desired source hashes; written
  only according to existing apply/flush semantics.
- SessionTarget/SessionSync: repository, branch, worktree, alias and ownership;
  current branch assertion, lock and explicit staging remain required.
- Upload readiness: identity progresses from uploaded to visible to renamed
  to settled; timeout/refusal never claims successful synchronization.
- Stray candidate: temporary title plus content digest; adoption requires
  equality against desired content and never relies on filename alone.
- Hosting declaration: account/profile and migration fields; resolution follows
  the existing environment, named assembly path and pinned path order.
