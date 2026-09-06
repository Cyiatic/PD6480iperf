import struct
import tempfile
from pathlib import Path
import unittest
from unittest.mock import patch

from inspect_modern_rdram import inspect, KEYS


class ModernRdramTests(unittest.TestCase):
    def snapshot(self, bad_layout=False, bad_code=False, buffers=3):
        offsets = [0x50443831, 1, 0x504, 12, 0x2ac, 0x4bc, 0x284, 0x2bc,
                   0x1c80, 0x1a34, 0x90, 0x18, 0x84, 0x2c, 0x18, 0x1a, 0x28,
                   0xa8, 0x88, 0x8c, 0x238, 0x10, 0x12, 0x11c, 0x120, 0x124]
        self.assertEqual(len(offsets), len(KEYS))
        if bad_layout:
            offsets[2] = 0x508
        symbols = {
            'g_Vars': (0x80002000, 0x504), 'g_Sched': (0x80002600, 0xa8),
            'g_MainThread': (0x80002800, 0x238), 'g_SchedThread': (0x80002b00, 0x238),
            'g_MempOnboardPools': (0x80003000, 180),
            'g_MempExpansionPools': (0x80003100, 180),
            'g_FrameBuffers': (0x80003200, buffers * 4),
        }
        for index, name in enumerate(('g_ViBackData', 'g_StageNum', 'var800844f0',
                                      'g_HiResEnabled', 'g_LvOom', 'g_LvOomSize',
                                      'g_PakHasEeprom', 'g_Rooms')):
            symbols[name] = (0x80003300 + index * 4, 4)
        symbols['mainLoop'] = (0x80001000, 8)

        class FakeElf:
            def symbol_data(self, name):
                return bytes.fromhex('12345678abcdef90')

        elf = FakeElf()
        elf.symbols = symbols
        ram = bytearray(0x800000)

        def word(address, value):
            struct.pack_into('<I', ram, address & 0x7fffff, value)

        def half(address, value):
            struct.pack_into('<h', ram, (address & 0x7fffff) ^ 2, value)

        ram[0x1000:0x1008] = bytes.fromhex('7856341290efcdab')
        if bad_code:
            ram[0x1000] ^= 1
        word(symbols['g_ViBackData'][0], 0x80004000)
        half(0x80004018, 640)
        half(0x8000401a, 480)
        word(0x80004028, 0x80400000)
        for index, pointer in enumerate((0x8036a000, 0x80400000, 0x8076a000)):
            word(0x80003200 + index * 4, pointer)
        word(0x80002000 + 0x284, 0x80005000)
        word(0x80005000 + 0x1a34, 3)  # new player ABI
        word(0x80005000 + 0x1a24, 99)  # old offset must not be used

        with tempfile.TemporaryDirectory(prefix='pd-modern-inspect-') as directory:
            directory = Path(directory)
            elf_path, ram_path, layout_path = [directory / name for name in ('elf', 'ram', 'layout')]
            elf_path.write_bytes(b'fake elf')
            ram_path.write_bytes(ram)
            layout_path.write_bytes(struct.pack('>' + 'I' * len(offsets), *offsets))
            with patch('inspect_modern_rdram.Elf32', return_value=elf):
                return inspect(elf_path, ram_path, layout_path)

    def test_candidate_layout_and_three_buffers(self):
        result = self.snapshot()
        self.assertEqual(result['active_dimensions'], [640, 480])
        self.assertEqual(result['player_pause_mode'], 3)
        self.assertEqual(len(result['framebuffers']), 3)
        self.assertFalse(result['hardware_verified'])

    def test_abi_mismatch_rejected(self):
        with self.assertRaisesRegex(ValueError, 'ABI mismatch'):
            self.snapshot(bad_layout=True)

    def test_buffer_count_comes_from_candidate_elf(self):
        self.assertEqual(len(self.snapshot(buffers=2)['framebuffers']), 2)

    def test_resident_code_mismatch_rejected(self):
        with self.assertRaisesRegex(ValueError, 'Resident code mismatch'):
            self.snapshot(bad_code=True)


if __name__ == '__main__':
    unittest.main()
