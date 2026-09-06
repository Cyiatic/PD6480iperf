import struct
import unittest
from audit_pad_cover_assets import cover_bounds


class PadCoverBoundsTests(unittest.TestCase):
    def test_valid(self):
        data = struct.pack('>5I', 0, 2, 20, 20, 20) + bytes(56 + 4)
        self.assertEqual(cover_bounds(data), 2)

    def test_overstated_count(self):
        data = struct.pack('>5I', 0, 425, 20, 20, 20) + bytes(200 * 28)
        with self.assertRaisesRegex(ValueError, 'count/bounds mismatch'):
            cover_bounds(data)

    def test_understated_count(self):
        data = struct.pack('>5I', 0, 1, 20, 20, 20) + bytes(56)
        with self.assertRaisesRegex(ValueError, 'count/bounds mismatch'):
            cover_bounds(data)

    def test_short_header(self):
        with self.assertRaisesRegex(ValueError, 'truncated'):
            cover_bounds(bytes(16))


if __name__ == '__main__':
    unittest.main()
