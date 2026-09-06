import unittest
from inspect_bgcache import validate_partition

class CacheInspectionTests(unittest.TestCase):
    def test_two_banks_exact_coverage(self):
        validate_partition([(0x80000000,64),(0x80400000,32)],
            [(0x80000000,16,'gfx'),(0x80000010,32,'batches'),(0x80000030,16,'free'),
             (0x80400000,32,'free')])

    def test_never_accept_missing_overlap_gap_or_unowned(self):
        for spans in ([], [(0x80000000,32,'gfx')], [(0x80000000,80,'gfx')],
                [(0x80000000,64,'gfx'),(0x80000010,16,'free')], [(0x80000001,64,'gfx')],
                [(0x80000000,63,'gfx')], [(0x80400000,64,'gfx')]):
            with self.subTest(spans=spans), self.assertRaises(ValueError):
                validate_partition([(0x80000000,64)],spans)

    def test_adjacent_and_disjoint_bank_rules(self):
        with self.assertRaises(ValueError):
            validate_partition([(0x80000000,64),(0x80000030,64)],[])
        with self.assertRaises(ValueError):
            validate_partition([(0x80000000,32),(0x80000040,32)],[(0x80000000,96,'cross-gap')])

if __name__ == '__main__': unittest.main()
