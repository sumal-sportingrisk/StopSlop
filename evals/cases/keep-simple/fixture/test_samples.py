from types import SimpleNamespace
import unittest

from samples import find_sample


class SampleTests(unittest.TestCase):
    def test_first_matching_object_is_returned(self):
        first = SimpleNamespace(id=1)
        second = SimpleNamespace(id=1)
        self.assertIs(find_sample([first, second], 1), first)

    def test_absence_is_none(self):
        self.assertIsNone(find_sample([], 3))
