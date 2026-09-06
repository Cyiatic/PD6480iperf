import tempfile
from pathlib import Path
import unittest
from unittest.mock import patch
from verify_resident_code import verify


class FakeElf:
    symbols = {name: (0x80001000, 8) for name in
               ['mainLoop', 'memaReset', 'memaAlloc', 'func0f004c6c', 'viReset']}

    def symbol_data(self, name):
        return bytes.fromhex('12345678abcdef90')


class ResidentCodeTests(unittest.TestCase):
    def run_snapshot(self, mutated=False, truncated=False):
        with tempfile.TemporaryDirectory(prefix='pd-resident-test-') as directory:
            path = Path(directory) / 'ram.bin'
            data = bytearray(8 * 1024 * 1024)
            data[0x1000:0x1008] = bytes.fromhex('7856341290efcdab')
            if mutated:
                data[0x1000] ^= 1
            path.write_bytes(data[:-1] if truncated else data)
            with patch('verify_resident_code.Elf32', return_value=FakeElf()):
                return verify('unused.elf', path)

    def test_matching_code(self):
        self.assertEqual(len(self.run_snapshot()), 5)

    def test_different_code(self):
        with self.assertRaisesRegex(ValueError, 'Resident code mismatch'):
            self.run_snapshot(mutated=True)

    def test_short_ram(self):
        with self.assertRaisesRegex(ValueError, '8 MiB'):
            self.run_snapshot(truncated=True)


if __name__ == '__main__':
    unittest.main()
