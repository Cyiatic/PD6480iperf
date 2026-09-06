import struct
import unittest
from assemble_modern_layout import assemble
from run_modern_menu_missions import validate_solo_seed


class MissionModeGateTests(unittest.TestCase):
    def test_solo(self):
        validate_solo_seed(dict(mission_configuration=dict(
            cooperative=False, counteroperative=False, ai_buddies=0)))

    def test_unknown_coop_counterop_and_ai_are_rejected(self):
        for config in (None, dict(cooperative=True, counteroperative=False, ai_buddies=1),
                       dict(cooperative=False, counteroperative=True, ai_buddies=0),
                       dict(cooperative=False, counteroperative=False, ai_buddies=1)):
            with self.subTest(config=config), self.assertRaises(ValueError):
                validate_solo_seed(dict(mission_configuration=config))

    def test_assembly(self):
        header = struct.pack('>73I', 0x50443831, 6, *([0] * 70), 24)
        probes = bytes(48)
        self.assertEqual(assemble(header, probes), header + probes)
        for h, p in ((header[:-4], probes), (header, probes[:-1]),
                     (bytes(len(header)), probes)):
            with self.assertRaises(ValueError):
                assemble(h, p)


if __name__ == '__main__':
    unittest.main()
