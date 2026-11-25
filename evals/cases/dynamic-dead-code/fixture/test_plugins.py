import unittest

from plugins import run_plugin


class PluginTests(unittest.TestCase):
    def test_registered_formatter(self):
        self.assertEqual(run_plugin("sample"), "SAMPLE")
