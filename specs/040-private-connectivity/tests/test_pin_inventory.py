"""Ownership failures must prevent an incomplete or ambiguous evidence census."""
import importlib.util
from pathlib import Path
import unittest

spec=importlib.util.spec_from_file_location("pilot_pin_inventory",Path(__file__).resolve().parents[1]/"register-evidence-pins.py")
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)

class PinInventoryTests(unittest.TestCase):
    def test_local_and_foreign_are_distinct_and_original_references_preserved(self):
        a="a"*40;b="b"*40
        record={"authority_ref":"git:"+a+":record.md","runtime_ref":"git:"+b+":runtime.json"}
        original=dict(record)
        rows=module.inventory(record,{"opensoft/openxFactory":{a},"opensoft/Headscale-Install":{b}})
        self.assertEqual(rows,[{"repository":"opensoft/openxFactory","openxfactory_commit":a},{"repository":"opensoft/Headscale-Install","foreign_commit":b}])
        self.assertEqual(record,original)
    def test_unknown_or_ambiguous_owner_never_becomes_a_foreign_exemption(self):
        a="a"*40
        for owners in ({"opensoft/openxFactory":set()},{"opensoft/openxFactory":{a},"other/repo":{a}}):
            with self.assertRaises(ValueError):module.inventory({"ref":"git:"+a+":record.md"},owners)

if __name__=="__main__":unittest.main()
