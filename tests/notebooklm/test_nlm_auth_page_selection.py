from __future__ import annotations

import unittest

from tests.notebooklm._test_nlm_auth_support import FakeContext, nlm_auth


class PageSelection(unittest.TestCase):
    """#537 harness half: both hosts count as NotebookLM."""

    def test_a_new_host_tab_is_selected(self) -> None:
        ctx = FakeContext(
            ["https://mail.google.com/", "https://notebook.google.com/notebook/abc"]
        )
        page, how = nlm_auth.select_notebooklm_page(ctx)
        self.assertEqual(how, "existing")
        self.assertEqual(page, ctx.pages[1])
        self.assertEqual(ctx.new_pages, 0)
        self.assertEqual(page.goto_calls, [])

    def test_an_old_host_tab_is_still_selected(self) -> None:
        ctx = FakeContext(["https://notebooklm.google.com/"])
        page, how = nlm_auth.select_notebooklm_page(ctx)
        self.assertEqual(how, "existing")
        self.assertEqual(page, ctx.pages[0])

    def test_no_notebooklm_tab_opens_a_new_one_and_hijacks_nothing(self) -> None:
        ctx = FakeContext(["https://docs.google.com/document/d/keep-me"])
        first = ctx.pages[0]
        page, how = nlm_auth.select_notebooklm_page(ctx)
        self.assertEqual(how, "new")
        self.assertEqual(ctx.new_pages, 1)
        self.assertIsNot(page, first)
        self.assertEqual(first.url, "https://docs.google.com/document/d/keep-me")
        self.assertEqual(first.goto_calls, [])

    def test_an_empty_browser_opens_a_tab(self) -> None:
        ctx = FakeContext([])
        _page, how = nlm_auth.select_notebooklm_page(ctx)
        self.assertEqual(how, "new")
        self.assertEqual(ctx.new_pages, 1)

    def test_the_predicate_matches_on_host_not_substring(self) -> None:
        self.assertTrue(nlm_auth.is_notebooklm_url("https://notebook.google.com/x"))
        self.assertTrue(nlm_auth.is_notebooklm_url("https://notebooklm.google.com/"))
        self.assertFalse(
            nlm_auth.is_notebooklm_url("https://evil.example/?q=notebook.google.com")
        )
        self.assertFalse(nlm_auth.is_notebooklm_url("https://mail.google.com/"))
        self.assertFalse(nlm_auth.is_notebooklm_url(""))
        self.assertFalse(nlm_auth.is_notebooklm_url(None))

    def test_NB_URL_stays_on_the_host_the_evidence_covers(self) -> None:
        self.assertEqual(nlm_auth.NB_URL, "https://notebooklm.google.com/")
        self.assertEqual(
            set(nlm_auth.NB_HOSTS), {"notebook.google.com", "notebooklm.google.com"}
        )
