import unittest

from config import effective_timeout


class TimeoutTests(unittest.TestCase):
    def test_absent_uses_default(self):
        self.assertEqual(effective_timeout(None), 30)

    def test_zero_disables_timeout(self):
        self.assertEqual(effective_timeout(0), 0)

    def test_explicit_timeout(self):
        self.assertEqual(effective_timeout(12), 12)
