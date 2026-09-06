import struct
import tempfile
from pathlib import Path
import unittest
from unittest.mock import patch

from inspect_modern_rdram import inspect, KEYS, V2_KEYS, V3_KEYS


class ModernRdramTests(unittest.TestCase):
    def snapshot(self, bad_layout=False, bad_code=False, buffers=3, gameplay=False,
                 truncate=False, replay=False, room_batches=False, missing_batches=False,
                 opaque=True, bad_batch_count=False, truncate_batches=False):
        gameplay = gameplay or room_batches
        offsets = [0x50443831, 1, 0x504, 12, 0x2ac, 0x4bc, 0x284, 0x2bc,
                   0x1c80, 0x1a34, 0x90, 0x18, 0x84, 0x2c, 0x18, 0x1a, 0x28,
                   0xa8, 0x88, 0x8c, 0x238, 0x10, 0x12, 0x11c, 0x120, 0x124]
        self.assertEqual(len(offsets), len(KEYS))
        if gameplay:
            offsets[1] = 2
            extra = [0xbc, 0xd8, 0xdc, 0x640, 0x900, 0x858, 0x17b8,
                     0x48, 8, 0x28, 0x1614]
            self.assertEqual(len(extra), len(V2_KEYS))
            if not truncate:
                offsets.extend(extra)
        if room_batches:
            offsets[1] = 3
            batch_extra = [0x44, 0x40, 32, 0x2c, 8, 12]
            self.assertEqual(len(batch_extra), len(V3_KEYS))
            if not truncate_batches:
                offsets.extend(batch_extra)
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
        if replay:
            for index, name in enumerate(('g_PdHwPhase', 'g_PdHwPhaseTicks',
                    'g_PdHwToggleChecks', 'g_PdHwSaveReads', 'g_PdHwSaveWrites')):
                symbols[name] = (0x80003400 + index * 4, 4)

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
        if replay:
            for index, value in enumerate((8, 123, 3, 45, 10)):
                word(0x80003400 + index * 4, value)
        if gameplay:
            word(0x800050bc, 0x80007500)
            for index, value in enumerate((12.5, -20.0, 45.25)):
                struct.pack_into('<f', ram, 0x7508 + index * 4, value)
            half(0x80007528, 9)
            half(0x8000752a, -1)
            struct.pack_into('<f', ram, 0x50dc, 0.75)
            word(0x80005000 + 0x640 + 0x858, 7)
            word(0x80005000 + 0x17b8 + 4, 184)
        if room_batches:
            word(symbols['g_Rooms'][0], 0x80008000)
            word(0x80002000 + 0x2bc, 2)
            word(0x80008090 + 0x18, 0x80009000)
            word(0x80009008, 0x80009100 if opaque else 0)
            word(0x80008090 + 0x44, 0 if missing_batches else 0x80009200)
            word(0x80008090 + 0x40, 0xffffffff if bad_batch_count or missing_batches else 252)

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

    def test_gameplay_fields_use_compiled_layout(self):
        result = self.snapshot(gameplay=True)
        self.assertEqual(result['player_position'], [12.5, -20, 45.25])
        self.assertEqual(result['player_rooms'], [9])
        self.assertEqual(result['player_health'], 0.75)
        self.assertEqual(result['loaded_ammo'][0][0], 7)
        self.assertEqual(result['reserve_ammo'][1], 184)

    def test_truncated_gameplay_layout_rejected(self):
        with self.assertRaisesRegex(ValueError, 'Truncated gameplay layout'):
            self.snapshot(gameplay=True, truncate=True)

    def test_synthetic_replay_is_explicitly_labelled(self):
        result = self.snapshot(replay=True)
        self.assertEqual(result['synthetic_replay_diagnostic'], dict(
            phase=8, phase_ticks=123, toggle_checks=3, ram_save_reads=45, ram_save_writes=10))
        self.assertFalse(result['hardware_verified'])
        self.assertNotIn('synthetic_replay_diagnostic', self.snapshot())

    def test_room_batch_pointer_and_word_sized_count(self):
        result = self.snapshot(room_batches=True)
        self.assertEqual(result['rooms_missing_vertex_batches'], [])
        self.assertEqual(result['room_allocations'][0]['numvtxbatches'], 252)

    def test_geometry_pointer_is_not_enough(self):
        result = self.snapshot(room_batches=True, missing_batches=True)
        self.assertEqual(result['loaded_rooms'], [1])
        self.assertEqual(result['rooms_missing_vertex_batches'], [1])
        self.assertIsNone(result['room_allocations'][0]['numvtxbatches'])

    def test_no_opaque_layer_does_not_require_batches(self):
        result = self.snapshot(room_batches=True, missing_batches=True, opaque=False)
        self.assertEqual(result['rooms_missing_vertex_batches'], [])

    def test_invalid_batch_count_rejected(self):
        with self.assertRaisesRegex(ValueError, 'vertex-batch count'):
            self.snapshot(room_batches=True, bad_batch_count=True)

    def test_truncated_batch_layout_rejected(self):
        with self.assertRaisesRegex(ValueError, 'Truncated room-batch layout'):
            self.snapshot(room_batches=True, truncate_batches=True)


if __name__ == '__main__':
    unittest.main()
