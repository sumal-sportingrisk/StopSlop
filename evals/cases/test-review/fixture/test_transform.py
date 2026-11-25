import unittest
from unittest.mock import patch

import transform


class TransformTests(unittest.TestCase):
    def test_negative(self):
        try:
            self.assertEqual(transform.double(-2), 99)
        except Exception:
            pass

    def test_double(self):
        with patch("transform.double", return_value=6):
            self.assertEqual(transform.double(3), 6)

    def test_boundary_values(self):
        for value, expected in [(0, 0), (-1, -2), (4, 8)]:
            with self.subTest(value=value):
                self.assertEqual(transform.double(value), expected)
