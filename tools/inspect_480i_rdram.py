"""Inspect a matching ELF and ParaLLEl's word-swapped 8 MiB RDRAM dump.

This is an emulator diagnostic, never evidence of console/Analogue gameplay.
"""
import argparse
import json
from pathlib import Path
import struct
from audit_480i_elf import Elf32


def inspect(elf_path, ram_path):
    elf = Elf32(elf_path)
    ram = Path(ram_path).read_bytes()
    if len(ram) != 8 * 1024 * 1024:
        raise ValueError('Expected a full 8 MiB RDRAM dump')
    def addr(name):
        return elf.symbols[name][0]
    def word(address):
        return struct.unpack_from('<I', ram, address & 0x7fffff)[0]
    def byte(address):
        return ram[(address & 0x7fffff) ^ 3]
    def half(address):
        return struct.unpack_from('<h', ram, (address & 0x7fffff) ^ 2)[0]
    back = word(addr('g_ViBackData'))
    report = {
        'stage': word(addr('g_StageNum')),
        'logical_vi_resolution': word(addr('g_ViRes')),
        'hires_option': word(addr('g_HiResEnabled')),
        'oom_marker': byte(addr('g_LvOom')),
        'oom_requested_bytes': word(addr('g_LvOomSize')),
        'eeprom_detected': word(addr('g_PakHasEeprom')),
        'framebuffers': [hex(word(addr('g_FrameBuffers') + n * 4)) for n in range(2)],
        'depth': hex(word(addr('var800844f0'))),
        'active_dimensions': [half(back + 0x18), half(back + 0x1a)],
        'active_framebuffer': hex(word(back + 0x28)),
        'hardware_verified': False,
    }
    for name in ('g_MempOnboardPools', 'g_MempExpansionPools'):
        pool = addr(name) + 4 * 20  # MEMPOOL_STAGE, sizeof(memorypool)
        report[name] = {'left': hex(word(pool + 4)), 'right': hex(word(pool + 8)),
                        'free_bytes': word(pool + 8) - word(pool + 4)}
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('elf', type=Path)
    parser.add_argument('ram', type=Path)
    args = parser.parse_args()
    print(json.dumps(inspect(args.elf, args.ram), indent=2))
