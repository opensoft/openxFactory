# NotebookLM Ideas: notebooklm-import-test

Status: brainstorm
Kind: reference
Repository context: openxFactory
Source workspace: test-canon
Source workspace id: 70647cc5-3929-486e-8d04-aad89a0f4adb
Authority: L1 notebook synthesis
Origin: NotebookLM note converted to source, then pulled by live MCP test.

These notes are imported evidence and idea material. They do not decide policy,
memory, release scope, or OpenSpec approval.

Import note: this source was not manually renamed. It represents the intended
real-life behavior: once a note is converted to a NotebookLM source, the source
is eligible to return to the brainstorm/staging folder that created the
analysis notebook.

## The codexFactory Governance Lifecycle and Sync Protocol

NotebookLM source id: 65e91c4d-5946-4683-a94d-a78886b07a95
NotebookLM source title: The codexFactory Governance Lifecycle and Sync Protocol
Source workspace: test-canon

The codexFactory Governance Lifecycle and Sync Protocol

Based on the sources, you cannot manually add a note or hand-curate sources
directly within this notebook [1]. The notebook is a "derived projection" of
the governance lifecycle and is maintained automatically by a script
(`scripts/sync-notebooklm-books.py`) in codexFactory, with membership determined
by each document's `Status` header [1].

Furthermore, any notes or output generated within this notebook itself are
considered "L1 notebook synthesis"; they can explore ideas and raise claims,
but they can "never decides policy, memory, or workflow" [2].

If you want to introduce a note for a new or modified feature, it must be added
to the underlying repository so the automated scripts can sync it into the
notebook. Here is how you should handle it:

Capture it in the Brainstorm Area:

Free-form thinking or new feature notes should be added to the repository's
`ideation/brainstorm/` directory, which brings the document into the lifecycle
at the `captured` state [3-5]. Once it is committed there with a
`Status: brainstorm` header, it will automatically become part of the notebook
[1, 6].

Beware of the Explicit Delta Rule:

You mentioned the note is not contradictory. However, you must still be careful
not to restate existing policy. Outside of the `ideation/brainstorm/` area, the
"Explicit Delta Rule" applies: any change, contradiction, or even restatement
of promoted policy in different words is treated as a defect [7-10].

Proposing a Change:

If your note is intended to act as a formal modification to the system, rather
than just a brainstorm, it must be expressed as an explicit change from the
current state. This requires an OpenSpec change proposal or an
`xspec:supersedes` marker naming the affected spec requirement [7, 9].

## NotebookLM hybrid import non-note live source

NotebookLM source id: f954f92f-e464-445a-98fc-46c6f9a2c15d
NotebookLM source title: NotebookLM hybrid import non-note live source
Source workspace: 70647cc5-3929-486e-8d04-aad89a0f4adb

Live acceptance source for xFactory NotebookLM hybrid imports. This source was
added directly as a NotebookLM text source, not created as a note, to prove
that non-note sources in a hybrid can be returned to the origin brainstorm
folder as L1 notebook synthesis.
