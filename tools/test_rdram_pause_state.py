"""Keep diagnostic pause reporting distinct from a mission-load pass."""
from pathlib import Path
import struct
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from inspect_480i_rdram import inspect


class PauseStateTests(unittest.TestCase):
    def snapshot(self, paused, mode, player=0x80020000, variables_size=0x504):
        names = ('g_ViBackData', 'g_StageNum', 'g_ViRes', 'g_HiResEnabled',
                 'g_LvOom', 'g_LvOomSize', 'g_PakHasEeprom', 'g_FrameBuffers',
                 'var800844f0', 'g_MempOnboardPools', 'g_MempExpansionPools',
                 'g_Vars', 'g_Rooms', 'g_MemaHeap', 'g_MissionConfig',
                 'var80084014')
        symbols = {name: (0x80001000 + i * 0x1000, 4)
                   for i, name in enumerate(names)}
        symbols['g_Vars'] = (symbols['g_Vars'][0], variables_size)
        ram = bytearray(8 * 1024 * 1024)

        def put(address, value):
            struct.pack_into('<I', ram, address & 0x7fffff, value)

        put(symbols['g_ViBackData'][0], 0x80030000)
        put(symbols['var80084014'][0], int(paused))
        put(symbols['g_Vars'][0] + 0x284, player)
        if player == 0x80020000:
            put(player + 0x1a24, mode)
        with patch('inspect_480i_rdram.Elf32', return_value=SimpleNamespace(symbols=symbols)), \
                patch.object(Path, 'read_bytes', return_value=bytes(ram)):
            return inspect('unused.elf', 'unused.bin')

    def test_paused_menu(self):
        result = self.snapshot(True, 3)
        self.assertTrue(result['level_paused'])
        self.assertEqual(result['player_pause_mode'], 3)

    def test_unpaused_play(self):
        result = self.snapshot(False, 0)
        self.assertFalse(result['level_paused'])
        self.assertEqual(result['player_pause_mode'], 0)

    def test_invalid_player_pointer_is_not_dereferenced(self):
        self.assertNotIn('player_pause_mode', self.snapshot(False, 0, player=0x3f800000))

    def test_unknown_variables_layout_is_not_guessed(self):
        self.assertNotIn('player_pause_mode', self.snapshot(False, 0, variables_size=0x500))


if __name__ == '__main__':
    unittest.main()
