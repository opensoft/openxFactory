# Corpus-adapter conformance fixtures

RULING OQ-3 (opensoft/openxFactory#656, 2026-09-06): **SEED HERE.** Design D6
part 3 of `split-opendox-two-layer-product` requires "a neutral conformance
corpus every destination passes" — "a corpus with no `openspec/`, no
`contracts/`, no lifecycle headers" — and says *every* destination, so
openXdox's adapter implementation and openxFactory's own adapter run it too.
That is the only mechanical proof that `corpus-adapter-seam`'s
no-privileged-route requirement holds for the home corpus.

`tasks.md` § 3.7 files that corpus on the openDox side, which does not exist
yet. `neutral/` is therefore the **seed handed upstream** when it does. It is
deliberately implementation-agnostic, and so is the suite that runs over it
(`../test_conformance.py`, parameterized by an adapter FACTORY), so handing the
pair to openDox is a move rather than a rewrite.

**This file is documentation ABOUT the fixtures and deliberately sits OUTSIDE
`neutral/`.** The neutral corpus must not contain the words it exists to prove
a reader does not need, and a document explaining that would contain every one
of them.

| fixture | shape | what it proves |
| --- | --- | --- |
| `neutral/` | two roots (`notes/`, `papers/`), three documents, a header vocabulary of its own (`Type:`, `Title:`) that belongs to no governed repository; `papers/gamma.md` carries no kind header | a reader authored for a governed corpus works over a corpus it does not own, and reports an unrecognizable document rather than omitting it |
| `empty/` | the declared roots present, zero documents | an empty corpus is an ANSWER, distinguishable from a refusal |
| `not-a-directory` | a file where a corpus is expected | resolution refuses UNREADABLE and names the path — `corpus_root.corpus_scan_defect`'s second defect, without `chmod`, which is unreliable as root on CI |
| *(absent)* | a path under `tmp_path` that is never created | resolution refuses ABSENT and names the corpus, rather than returning an empty document list |

`neutral/` declares NO governed write path, so it is read-only and a write-back
must say so at resolution time rather than failing at dispatch.
