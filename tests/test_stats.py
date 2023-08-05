from unittest import TestCase

from ed_utils.decorators import number, visibility
from ed_utils.timeout import timeout

from stats import SimpleStats, ComplexStats

from data_structures.referential_array import ArrayR

class TestStats(TestCase):

    @number("1.1")
    @visibility(visibility.VISIBILITY_SHOW)
    @timeout()
    def test_simple_stats(self):
        ss = SimpleStats(8, 2, 4, 12)
        self.assertEqual(ss.get_attack(), 8)
        self.assertEqual(ss.get_defense(), 2)
        self.assertEqual(ss.get_speed(), 4)
        self.assertEqual(ss.get_max_hp(), 12)

    @number("4.3")
    @visibility(visibility.VISIBILITY_SHOW)
    @timeout()
    def test_complex_stats(self):
        cs = ComplexStats(
            ArrayR.from_list([
                "5",
                "6",
                "+"
            ]),
            ArrayR.from_list([
                "9",
                "2",
                "8",
                "middle"
            ]),
            ArrayR.from_list([
                "level",
                "3",
                "power",
                "1",
                "2",
                "3",
                "middle",
                "*"
            ]),
            ArrayR.from_list([
                "level",
                "5",
                "-",
                "sqrt",
                "1",
                "10",
                "middle",
            ]),
        )
        self.assertEqual(cs.get_attack(1), 11)
        self.assertEqual(cs.get_defense(1), 8)
        self.assertEqual(cs.get_speed(5), 250)
        self.assertEqual(cs.get_max_hp(41), 6)
