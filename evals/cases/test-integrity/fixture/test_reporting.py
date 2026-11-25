import unittest

from reporting import round_report_value


class RoundingTests(unittest.TestCase):
    def test_half_rounds_up(self):
        self.assertEqual(round_report_value(2.5), 3)

    def test_negative_half_rounds_away_from_zero(self):
        self.assertEqual(round_report_value(-2.5), -3)

    def test_two_places(self):
        self.assertEqual(round_report_value(0.125, 2), 0.13)

    def test_below_half(self):
        self.assertEqual(round_report_value(1.4), 1)
