import unittest

from summary import summarize


class SummaryTests(unittest.TestCase):
    def test_count(self):
        self.assertEqual(summarize("samples.json"), {"count": 2})
