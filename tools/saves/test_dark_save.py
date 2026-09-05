"""Run with python -m unittest discover -s tools/saves -v."""
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest
import make_dark_save as save


class DarkSaveTests(unittest.TestCase):
    def test_deterministic_image_and_checksums(self):
        data = save.generate()
        self.assertEqual(data, save.generate())
        self.assertEqual(save.validate(data)['sha256'],
                         'fa86c003d8cf71cb099c2c55a92cdea3f00b4d482370a48202d7a0d4b0184a7d')

    def test_corruption_rejected(self):
        for offset in (0, 8, 16, 0xE0 + 16, 0x450 + 16, 0x7C0):
            with self.subTest(offset=offset):
                data = bytearray(save.generate())
                data[offset] ^= 1
                with self.assertRaises((ValueError, AssertionError)):
                    save.validate(data)
        with self.assertRaises(ValueError):
            save.validate(save.generate()[:-1])

    def test_wont_overwrite_a_save(self):
        with tempfile.TemporaryDirectory(prefix='pd-dark-save-test-') as directory:
            target = Path(directory) / 'existing.eep'
            target.write_bytes(b'user save sentinel')
            result = subprocess.run([sys.executable, save.__file__, str(target)],
                                    capture_output=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(target.read_bytes(), b'user save sentinel')

    def test_cheat_targets_against_decomp_when_available(self):
        # Optional source audit; the published generator needs no decomp/ROM.
        source = Path(__file__).resolve().parents[3] / 'pd-upstream-latest' / 'src'
        if not source.exists():
            self.skipTest('Sibling stock decomp checkout not present')
        constants = (source / 'include/constants.h').read_text()
        stages = {name: int(value, 16) for name, value in re.findall(
            r'#define (SOLOSTAGEINDEX_\w+)\s+(0x[0-9a-fA-F]+)', constants)}
        cheats = (source / 'game/cheats.c').read_text().split('u32 cheat_is_unlocked')[0]
        targets = {}
        # Each conditional lists NTSC-final first, then the beta alternative.
        for minutes, seconds, stage, difficulty in re.findall(
                r'TIME\((\d+) m,\s*(\d+) s\),\s*(SOLOSTAGEINDEX_\w+),\s*DIFF_(A|SA|PA),', cheats):
            key = stages[stage], {'A': 0, 'SA': 1, 'PA': 2}[difficulty]
            targets.setdefault(key, int(minutes) * 60 + int(seconds))
        self.assertEqual(targets, {(s, d): t for s, d, t in save.CHEAT_TARGETS})


if __name__ == '__main__':
    unittest.main()
